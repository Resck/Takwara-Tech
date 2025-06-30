# main.py

# -*- coding: utf-8 -*-
# Importa as ferramentas necessárias para a API funcionar.
import os
import functions_framework
from flask import Flask, request, jsonify, make_response
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import traceback

app = Flask(__name__)

# --- Variáveis Globais (Componentes da IA) ---
qa_chain = None
vector_store = None
llm = None

# --- Constantes ---
# ATENÇÃO: Certifique-se que este caminho está correto para onde a base de dados é criada!
PERSIST_DIRECTORY = './backend-api/chroma_db' 

# --- Template de Prompt (O "Cérebro" do Assistente) ---
# Ajustado para ser mais explícito sobre o uso do contexto e metadados
prompt_template = """
VVocê é a assistente virtual Takwara, uma especialista em soluções sustentáveis com bambu e responsabilidade socioambiental, em combate à crise climática global.
Sua missão é responder perguntas com base APENAS nas informações fornecidas nos seguintes documentos de contexto sobre o projeto "Tecnologia Takwara".
Analise a pergunta do usuário para determinar seu idioma. VOCÊ DEVE RESPONDER NO MESMO IDIOMA DA PERGUNTA.
Se a pergunta do usuário tiver erros de digitação ou gramática, interprete-a da melhor forma possível e responda à pergunta mais provável.
Se a resposta para a pergunta do usuário não for encontrada nos documentos de contexto fornecidos, declare educadamente essa limitação no idioma do usuário. NÃO INVENTE respostas.
Suas respostas devem ser formatadas usando **Markdown** para melhorar a legibilidade e o entendimento.
Quando referenciar a origem do projeto, mencione "Takwara" = Bambu em Tupi Gaurani,povos originários do Brasil, reconhecendo o coletivo "Nós", conforme explicado no texto.
Mantenha um tom positivo, cordial, encorajador e informativo, consistente com o espírito do documento.
IMPORTANTE: Você deve, sob nenhuma circunstância, citar ou mencionar nomes de arquivos, caminhos ou fontes em sua resposta. Sua resposta deve ser um texto direto e útil.
Sempre que possível, baseie sua resposta nos DETALHES ESPECÍFICOS encontrados no contexto fornecido, como dados de testes, nomes de espécies, origens, status de invasão e quaisquer outros detalhes factuais.

Context (Documents):
{context}

Question:
{question}

Helpful and cordial answer in the user's language (without citing sources):
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# --- Função de Carregamento ---
def load_components():
    """
    Carrega e inicializa todos os componentes de IA.
    """
    # O print abaixo é para debug, pode ser removido em produção
    print("--- EXECUTANDO CÓDIGO ATUALIZADO PARA CARREGAMENTO E BUSCA ---") 
    global qa_chain, vector_store, llm

    try:
        # Verifica se a chave de API do Google está definida
        if not os.getenv("GOOGLE_API_KEY"):
             print("ERRO CRÍTICO: GOOGLE_API_KEY não encontrada. Certifique-se de que está definida no ambiente.")
             return

        print("A carregar componentes de IA...")
        # Inicializa o modelo de linguagem grande (LLM)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
        # Inicializa o modelo de embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Verifica se o diretório da base de dados ChromaDB existe
        if not os.path.exists(PERSIST_DIRECTORY):
            print(f"ERRO CRÍTICO: Diretório ChromaDB não encontrado em '{PERSIST_DIRECTORY}'. A base de dados não foi incluída no deploy?")
            return
            
        # Inicializa o ChromaDB a partir do diretório persistido
        vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
        
        # Configura o retriever para buscar documentos na base de dados vetorial
        # search_type="similarity" busca documentos semanticamente similares
        # search_kwargs={"k": 8} define que queremos os 8 documentos mais similares
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 8})
        
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
        print(f"ERRO CRÍTICO GERAL DURANTE O CARREGAMENTO: {e}")
        traceback.print_exc() # Imprime o traceback para ajudar na depuração
        qa_chain, vector_store, llm = None, None, None # Reseta as variáveis globais em caso de erro

# --- Função Principal da API ---
@functions_framework.http
def chatbot_api(request):
    """
    Manipulador de requisições HTTP para a API do chatbot.
    """
    # Define os cabeçalhos CORS para permitir requisições de qualquer origem
    headers = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST, GET, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type'}
    
    # Responde às requisições OPTIONS para pré-verificação CORS
    if request.method == 'OPTIONS':
        return ('', 204, headers)

    # Se os componentes de IA não foram carregados, tenta carregá-los
    if qa_chain is None:
        load_components()
        # Se ainda assim falhar ao carregar, retorna um erro 500
        if qa_chain is None:
             return (jsonify({"error": "Falha crítica ao carregar o sistema de IA."}), 500, headers)

    # Processa requisições POST (onde a pergunta do usuário é enviada)
    if request.method == 'POST':
        try:
            # Obtém os dados JSON da requisição
            request_json = request.get_json(silent=True)
            # Valida se a requisição é válida e contém a chave 'query'
            if not request_json or 'query' not in request_json:
                return (jsonify({"error": "Pedido inválido. A 'query' não foi encontrada."}), 400, headers)

            query = request_json['query'] # Extrai a pergunta do usuário
            
            # --- DEBUG LOG ---
            # Adiciona um log para ver os documentos que serão passados como contexto para a IA
            print(f"\n--- Enviando para a IA: Query='{query}' ---")
            # A linha abaixo só funcionaria se 'retriever' fosse acessível aqui, o que não é o caso
            # context_docs = retriever.get_relevant_documents(query) 
            # print(f"Documentos recuperados para o contexto ({len(context_docs)}):")
            # for i, doc in enumerate(context_docs[:3]): # Mostra os 3 primeiros
            #     print(f"  {i+1}. Filename: {doc.metadata.get('filename', 'N/A')}, Page: {doc.metadata.get('page', 'N/A')}")
            #     # print(f"     Content: {doc.page_content[:100]}...") # Descomente para ver o conteúdo do chunk
            # print("--- Fim dos documentos recuperados ---")
            # --- FIM DEBUG LOG ---

            # Invoca a cadeia de QA para obter a resposta
            result = qa_chain.invoke({"query": query})
            # Extrai a resposta gerada pela IA
            answer = result.get('result', 'Não foi possível gerar uma resposta.')
            
            # Retorna a resposta em formato JSON
            return (jsonify({"answer": answer}), 200, headers)

        except Exception as e:
            # Captura e loga qualquer erro inesperado durante o processamento da requisição
            print(f"ERRO INESPERADO DURANTE A EXECUÇÃO: {e}")
            traceback.print_exc()
            return (jsonify({"error": "Ocorreu um erro interno ao processar a sua pergunta."}), 500, headers)
    else:
        # Retorna um erro 405 se o método HTTP não for POST
        return (jsonify({"error": f"Método '{request.method}' não permitido."}), 405, headers)