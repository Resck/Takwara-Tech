# -*- coding: utf-8 -*-
"""
VERSÃO FINAL AJUSTADA:
- Foco em persistência LOCAL do ChromaDB.
- Remoção completa de dependências e lógica do GCS.
- Busca contextual baseada nos metadados de URL dos arquivos .md.
- Prompt revisado para priorizar detalhes e NÃO citar fontes.
"""

import os
import functions_framework
from flask import Flask, request, jsonify, make_response
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever # Para múltiplas consultas
from langchain_core.documents import Document # Para trabalhar com documentos
import traceback # Para logar erros detalhados
from pathlib import Path # Para manipulação de caminhos de arquivo
from urllib.parse import quote # Para codificar caracteres especiais em URLs

app = Flask(__name__)

# --- Variáveis Globais para Componentes da IA ---
qa_chain = None
vector_store = None
embeddings = None
llm = None

# --- Constantes de Configuração ---
# AJUSTE CRÍTICO: O caminho na nuvem será direto para a pasta.
PERSIST_DIRECTORY = './chroma_db' 
# URL base do site para metadados de URL dos arquivos .md
BASE_URL_SITE = "https://resck.github.io/Takwara-Tech/" 

# --- Template de Prompt (O "Cérebro" da AVT) ---
# Ajustado para focar em detalhes específicos e evitar citações de fontes
prompt_template = """
You are a helpful and cordial virtual assistant Takwara, an expert in sustainable soluction for use bamboo and socio-environmental responsibility, against the global climate crise.

Your mission is to answer questions based ONLY on the information provided in the following context documents about the "Tecnologia Takwara" project.

Analyze the user's question to determine its language. YOU MUST RESPOND IN THE SAME LANGUAGE AS THE QUESTION.
If the user's question has spelling or grammatical errors, interpret it to the best of your ability and answer the most likely intended question.
If the answer to a user's question is not found within the provided context documents, politely state this in the user's language.

When answering user queries, strive for the following qualities:

* **Didactic:** Explain concepts clearly and logically, breaking down complex ideas found in the text (like the methodology components, the workflow, or the impact potential) into easily digestible parts. Use the structure and examples provided in the document to guide your explanations.
* **Engaging:** Use language that captures interest and reflects the passion and vision expressed in the text (e.g., the urgency of the challenge, the potential for transformation, the collaborative spirit). You can use metaphors or analogies suggested by the text (like "aço vegetal" or "solda verde"). Frame the information in a way that connects with the user's potential interest areas (architecture, engineering, sustainability, community work).
* **Stimulating:** Encourage the user's curiosity about the technology and its potential. Highlight the innovation and the forward-looking aspects.
* **Creative & Interpretative:** Go beyond simply repeating phrases. Interpret the meaning and significance of the information *within the context of the document*. For example, when explaining a methodology component, explain *why* it's innovative or *what problem* it solves, according to the text. Connect different parts of the document where relevant (e.g., how the ecological treatment supports the use in geodésicas, or how ecomaterials address waste and contribute to ODS). Explain the *implications* of the information presented.

**Specific Instructions & Interaction Style:**

* Your responses must be formatted using **Markdown** to improve readability and understanding.
* Never provide simplistic answers when there is ample content available in the context documents. Always refer to the source documents to extract and present the maximum relevant information for each query, summarizing and synthesizing information from various relevant sections.
* As an assistant, you will encourage the user to ask more complex and specific questions. Occasionally conclude your response with a thought-provoking statement, a question for further exploration, or by suggesting related areas based on the information discussed (e.g., "This section talks about ecomaterials. Would you like to know more about the specific types of waste used, or perhaps how they contribute to the ODS mentioned?").
* When referencing the project's origin or creator, mention Fabio "Takwara" Resck as the idealizer, acknowledging the collective "Nós" as explained in the text (the spirit of collaboration and all contributors, past and present).
* Mention that the material is open knowledge licensed under Creative Commons Attribution 4.0 International (CC BY 4.0) when discussing sharing, use, or contribution.
* Maintain a positive, cordial, encouraging, and informative tone consistent with the document's spirit.
* **IMPORTANT: DO NOT CITE ANY SOURCES OR FILE PATHS IN YOUR ANSWERS.** If you find information, present it directly without attribution to specific documents or paths.
* **PRIORITIZE EXTRACTION OF SPECIFIC DETAILS:** Always strive to extract detailed and concrete information from the retrieved documents, such as test results, numerical data, application methods, species names, etc.

Your ultimate goal is to be a comprehensive, engaging, and inspiring guide to the "Tecnologia Takwara" project, empowering users by clearly and thoroughly explaining its principles, methodologies, and potential, always rooted in the provided documentation.

Context (Documents):
{context}

Question:
{question}

Helpful and cordial answer in the user's language (without citing sources):
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# --- Função de Carregamento dos Componentes de IA ---
def load_components():
    """
    Carrega e inicializa todos os componentes de IA localmente.
    """
    print("--- EXECUTANDO CÓDIGO ATUALIZADO PARA CARREGAMENTO LOCAL ---") 
    global qa_chain, vector_store, llm, embeddings # Declaração para usar as globais

    try:
        # Verifica se a chave de API do Google está definida
        if not os.getenv("GOOGLE_API_KEY"):
             print("ERRO CRÍTICO: GOOGLE_API_KEY não encontrada. Certifique-se de que está definida no ambiente da Cloud Function.")
             return # Retorna None se a chave não estiver definida

        print("A carregar modelo de embeddings...")
        # Inicializa o modelo de embeddings do Google
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        print("Modelo de embeddings carregado.")

        # Verifica se o diretório da base de dados ChromaDB local existe
        if not os.path.exists(PERSIST_DIRECTORY):
            print(f"ERRO CRÍTICO: Diretório ChromaDB local não encontrado em '{PERSIST_DIRECTORY}'.")
            print("Por favor, execute o script create_vector_store.py para criá-lo.")
            return # Retorna None se o diretório não existir
            
        print(f"A carregar a base de vetores ChromaDB local de '{PERSIST_DIRECTORY}'...")
        # Inicializa o ChromaDB a partir do diretório local persistido
        vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
        print("Base de vetores ChromaDB carregada localmente.")
        
        # Configura o retriever para buscar documentos na base de dados vetorial local
        # search_type="similarity" busca documentos semanticamente similares
        # search_kwargs={"k": 8} define que queremos os 8 documentos mais similares
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 8})
        
        # Inicializa o modelo de linguagem grande (LLM)
        print("A carregar modelo LLM...")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
        print("Modelo LLM carregado.")
        
        # Cria a cadeia de perguntas e respostas (RetrievalQA chain)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, # O modelo de linguagem a ser usado
            chain_type="stuff", # Método para juntar os documentos recuperados
            retriever=retriever, # O retriever configurado
            chain_type_kwargs={"prompt": PROMPT}, # O prompt a ser usado
            return_source_documents=False # Não retornamos os documentos fonte na resposta final
        )
        print(">>> Componentes de IA carregados com sucesso! <<<")

    except Exception as e:
        # Captura e loga qualquer erro durante o carregamento dos componentes
        print(f"ERRO CRÍTICO GERAL DURANTE O CARREGAMENTO DOS COMPONENTES: {e}")
        traceback.print_exc() # Imprime o traceback para ajudar na depuração
        qa_chain, vector_store, llm, embeddings = None, None, None, None # Reseta as variáveis globais em caso de erro

# --- Função Principal da API ---
@functions_framework.http
def chatbot_api(request):
    """
    Manipulador de requisições HTTP para a API do chatbot.
    """
    # Define os cabeçalhos CORS para permitir requisições de qualquer origem
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }
    
    # Responde às requisições OPTIONS para pré-verificação CORS
    if request.method == 'OPTIONS':
        response = make_response('', 204)
        response.headers.extend(headers)
        return response

    # Se os componentes de IA não foram carregados, tenta carregá-los
    if qa_chain is None:
        load_components()
        # Se ainda assim falhar ao carregar, retorna um erro 500
        if qa_chain is None:
             print("Falha ao carregar os componentes de IA. Verifique os logs e a configuração.")
             return (jsonify({"error": "O sistema de IA falhou ao carregar. Verifique os logs da função."}), 500, headers)

    # Processa requisições POST (onde a pergunta do usuário é enviada)
    if request.method == 'POST':
        try:
            # Obtém os dados JSON da requisição
            request_json = request.get_json(silent=True)
            # Valida se a requisição é válida e contém a chave 'query'
            if not request_json or 'query' not in request_json:
                print("Pedido inválido: JSON ausente ou sem 'query'.")
                return (jsonify({"error": "Pedido inválido. Por favor, forneça uma pergunta no corpo JSON."}), 400, headers)

            query = request_json['query']
            # Captura o contexto da página, se fornecido (para busca contextual)
            context_url = request_json.get('context') 

            # --- Lógica para Saudações ---
            if query.lower().strip() in ["olá", "oi", "ola", "hello", "hi"]:
                try:
                     if llm is not None:
                          # Usa o LLM para gerar uma saudação mais dinâmica e contextualizada
                          greeting_prompt_text = f"Gere uma saudação cordial e breve no idioma da pergunta '{query}' ou no idioma padrão português, apresente-se como a assistente virtual Takwara, expert em construção sustentável com bambu, e pergunte como pode ajudar."
                          llm_greeting_response = llm.invoke(greeting_prompt_text)
                          greeting_text = llm_greeting_response.content
                          return (jsonify({"answer": greeting_text}), 200, headers)
                     else:
                          # Saudação padrão caso o LLM não esteja disponível
                          return (jsonify({"answer": "Olá! Sou a assistente virtual Takwara. Como posso te ajudar hoje?"}), 200, headers)
                except Exception as e:
                     print(f"AVISO: Erro ao tentar gerar saudação com LLM: {e}. Retornando saudação padrão.")
                     return (jsonify({"answer": "Olá! Sou a assistente virtual Takwara. Como posso te ajudar hoje?"}), 200, headers)
            
            # --- Lógica Principal de Consulta ---
            # Verifica se o vector_store foi carregado corretamente
            if vector_store is None:
                 print("ERRO: Vector store não está carregado. Não é possível realizar busca.")
                 raise RuntimeError("Vector store not loaded.")

            retrieved_docs = [] # Lista para armazenar os documentos recuperados
            
            # Normaliza a URL do contexto para garantir consistência na busca
            normalized_context_url = None
            if context_url and context_url != "/" and context_url != "/chatbot/":
                normalized_context_url = context_url if context_url.endswith('/') else context_url + '/'
            
            # --- Lógica de Busca Contextual ---
            # Se temos uma URL de contexto válida, tentamos buscar documentos específicos dela.
            if normalized_context_url:
                print(f"Buscando documentos com URL de contexto: {normalized_context_url}")
                
                # Realiza a busca no ChromaDB local com filtro de metadados para a URL.
                # O ChromaDB suporta filtros de metadados diretamente na busca.
                try:
                    relevant_docs_from_context = vector_store.similarity_search(
                        query=query,
                        k=8, # Recupera os 8 documentos mais similares (ajustado para priorizar detalhes)
                        filter={"url": normalized_context_url} # Filtra pelos metadados onde a URL corresponde
                    )
                    
                    if relevant_docs_from_context:
                        print(f"Encontrados {len(relevant_docs_from_context)} documentos no contexto '{normalized_context_url}'.")
                        retrieved_docs = relevant_docs_from_context
                    else:
                        print(f"Nenhum documento encontrado especificamente para o contexto '{normalized_context_url}'. Buscando globalmente.")
                        # Fallback para busca global se nenhum documento no contexto específico for encontrado
                        retrieved_docs = vector_store.similarity_search(query=query, k=8) # Usa o mesmo k para consistência
                
                except Exception as search_error: # Captura erros durante a busca
                    print(f"Erro durante a busca contextual (URL: {normalized_context_url}): {search_error}. Buscando globalmente.")
                    traceback.print_exc()
                    retrieved_docs = vector_store.similarity_search(query=query, k=8) # Fallback para busca global
            
            else: # Se não há contexto URL válido (ou é página inicial), busca globalmente
                print("Nenhum contexto URL válido fornecido ou é a página inicial. Buscando globalmente.")
                retrieved_docs = vector_store.similarity_search(query=query, k=8)

            # Se nenhuma busca retornou documentos (nem contextual nem global)
            if not retrieved_docs:
                print("Nenhum documento recuperado para a pergunta.")
                return (jsonify({"answer": "Não consegui encontrar informações relevantes sobre isso. Poderia reformular a pergunta ou me dar mais contexto?"}), 200, headers)
            
            # --- Invoca a cadeia RAG com os documentos recuperados ---
            # O prompt já está configurado para priorizar detalhes e não citar fontes.
            result = qa_chain.invoke({
                 "input_documents": retrieved_docs, # Documentos recuperados para gerar a resposta
                 "question": query
            })

            answer = result.get('output_text', 'Não foi possível extrair uma resposta útil dos documentos.')
            
            return (jsonify({"answer": answer}), 200, headers)

        except RuntimeError as e: # Erros específicos de tempo de execução (ex: vector_store not loaded)
            print(f"ERRO DE TEMPO DE EXECUÇÃO: {e}")
            return (jsonify({"error": str(e)}), 500, headers)
        except Exception as e: # Captura outros erros inesperados
            print(f"ERRO INESPERADO DURANTE O PROCESSAMENTO DA PERGUNTA: {e}")
            traceback.print_exc() # Log detalhado do erro
            return (jsonify({"error": f"Ocorreu um erro interno ao processar sua pergunta. Por favor, tente novamente mais tarde."}), 500, headers)
    else:
        # Retorna erro 405 para métodos HTTP não permitidos
        print(f"Método HTTP não permitido recebido: {request.method}")
        return (jsonify({"error": f"Método '{request.method}' não permitido."}), 405, headers)