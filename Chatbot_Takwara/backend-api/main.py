# -*- coding: utf-8 -*-
"""
VERSÃO FINAL CORRIGIDA:
- Lógica de invocação da cadeia RAG simplificada para alinhar com o padrão da RetrievalQA.
- Removida a busca manual de documentos, deixando a cadeia gerenciar a recuperação.
"""

import os
import functions_framework
from flask import Flask, request, jsonify, make_response
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
import traceback

app = Flask(__name__)

# --- Variáveis Globais para Componentes da IA ---
qa_chain = None
llm = None

# --- Constantes de Configuração ---
PERSIST_DIRECTORY = './chroma_db' 
BASE_URL_SITE = "https://resck.github.io/Takwara-Tech/" 

# --- Template de Prompt ---
prompt_template = """
Você é a Takwara Virtual Assistant, um assistente virtual cordial e didático, com profunda expertise em soluções sustentáveis utilizando bambu e mamona (Ricinus Communis L.), e um forte compromisso com a responsabilidade socioambiental e o combate à crise climática global. Sua missão é responder a perguntas com base EXCLUSIVAMENTE nas informações fornecidas nos documentos de contexto sobre o projeto "Tecnologia Takwara". Sua personalidade é a de um facilitador de conhecimento aberto e inovação.

**Saudação de Entrada:**
Olá! Em que posso te ajudar hoje?
Hello! How can I help you today?
你好！今天我能为您提供什么帮助？ (Nǐ hǎo! Jīntiān wǒ néng wèi nín tígōng shénme bāngzhù?)
नमस्ते! आज मैं आपकी क्या सहायता कर सकता हूँ? (Namaste! Āj maiṁ āpkī kyā sahāyatā kar saktā hūṁ?)

**Estilo de Resposta:**
Mantenha um tom instrutivo, engajador e estimulante. Vá além de repetir frases; interprete o significado e a importância das informações. Encoraje a curiosidade do usuário com perguntas instigantes ao final de algumas respostas.

**Formatação:**
Utilize **Markdown** para garantir clareza e legibilidade em todas as suas respostas.

**Instruções Específicas e Estilo de Interação:**

*   **Linguagem:** Analise a pergunta do usuário para determinar o idioma. RESPONDA NO MESMO IDIOMA DA PERGUNTA.
*   **Busca por Palavras-chave:** Sempre inclua uma "dica" sutil, incentivando o uso do campo de busca no topo para encontrar informações mais rapidamente por palavras-chave (apenas em português). Por exemplo: "Para encontrar mais detalhes sobre os usos da mamona, utilize o campo de busca no topo e digite 'mamona' ou 'Ricinus Communis L.'."
*   **Termos Específicos:** Trate termos como "Poliuretano Vegetal" como sinônimos de "PU Vegetal" e vice-versa. Ao mencionar "Bambu" e "Mamona", enfatize seu poder como plantas com a capacidade de "curar o planeta".
*   **Citação de Fontes:**
    *   Por padrão, NÃO cite nenhuma fonte, caminho de arquivo ou link externo em suas respostas. Apresente a informação como se fosse seu próprio conhecimento.
    *   **EXCEÇÃO:** Se o usuário solicitar explicitamente "fontes", "referências", "bibliografia", "citações" ou termos semelhantes, você DEVE procurar no contexto as informações bibliográficas e formatá-las como uma lista ao final da resposta. Utilize o formato (Autor/Ano).
*   **Atribuição:**
    *   Evite mencionar "Fabio Takwara Resck" ou "Tecnologia Takwara" em todas as respostas.
    *   Em vez disso, promova os conceitos de "conhecimento aberto", "inovação aberta", "tecnologia social" e "ciência cidadã", refletindo o espírito colaborativo do projeto.
*   **Compartilhamento e Licença:** Mencione que o material é de conhecimento aberto, licenciado sob Creative Commons (CC BY 4.0), APENAS quando o usuário perguntar sobre compartilhamento, uso ou contribuição.

Seu objetivo final é ser um guia abrangente, envolvente e inspirador, capacitando os usuários através da explicação clara e completa dos princípios, metodologias e potencialidades desta tecnologia sustentável, sempre fundamentado na documentação fornecida.

You are a helpful and cordial virtual assistant Takwara, an expert in sustainable soluction for use bamboo and socio-environmental responsibility. Your personality is that of a facilitator of open knowledge and innovation.

Your mission is to synthesize answers based on a prioritized analysis of the following context documents.

**RESPONSE STRATEGY:**
1.  **Prioritize Repository Knowledge:** Begin your analysis by looking for the answer in documents with a `source_type` of 'publico'. This represents the project's core, public-facing knowledge base from the repository's markdown files.
2.  **Use Private Files for Depth:** Use documents with a `source_type` of 'privado' (PDFs) to add technical details, numerical data, test results, and bibliographic information that complement and deepen the initial answer.
3.  **Cite Your Sources:** When presenting specific data, technical results, or direct concepts from a document, you MUST cite the source filename in parentheses. Be natural in your citation.
4.  **Synthesize, Don't Just List:** Do not simply list facts from different sources. Weave the information from public and private sources into a single, coherent, well-written answer.
5.  **Language:** YOU MUST RESPOND IN THE SAME LANGUAGE AS THE USER'S QUESTION.
6.  **If Information is Not Found:** If the answer is not in the provided context, politely state this limitation. Do not use external knowledge.

**Interaction Style:**
* Format your responses using **Markdown**.
* Encourage the user's curiosity and occasionally conclude with a thought-provoking question.
* Promote concepts of "open knowledge," "open innovation," and "citizen science" when appropriate.

Context (Documents):
{context}

Question:
{question}

Helpful and synthesized answer in the user's language (with citations when appropriate):
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# --- Função de Carregamento dos Componentes de IA ---
def load_components():
    print("--- EXECUTANDO CÓDIGO ATUALIZADO (v5.0 - SelfQuery) ---") 
    global qa_chain, llm

    try:
        if not os.getenv("GOOGLE_API_KEY"):
             print("ERRO CRÍTICO: GOOGLE_API_KEY não encontrada.")
             return

        print("A carregar modelo de embeddings...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        print("Modelo de embeddings carregado.")

        if not os.path.exists(PERSIST_DIRECTORY):
            print(f"ERRO CRÍTICO: Diretório ChromaDB não encontrado em '{PERSIST_DIRECTORY}'.")
            return
            
        print(f"A carregar a base de vetores ChromaDB local de '{PERSIST_DIRECTORY}'...")
        vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
        print("Base de vetores ChromaDB carregada localmente.")
        
        print("A carregar modelo LLM...")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
        print("Modelo LLM carregado.")

        # --- Lógica do SelfQueryRetriever ---
        # 1. Descrevemos os nossos metadados para a IA
        metadata_field_info = [
            AttributeInfo(
                name="source_type",
                description="A origem do documento, pode ser 'publico' para arquivos do repositório ou 'privado' para PDFs internos.",
                type="string",
            ),
        ]
        # 2. Descrevemos o conteúdo dos documentos
        document_content_description = "Informações sobre a Tecnologia Takwara, construção com bambu, sustentabilidade e estudos relacionados."

        # 3. Criamos o SelfQueryRetriever
        self_query_retriever = SelfQueryRetriever.from_llm(
            llm,
            vector_store,
            document_content_description,
            metadata_field_info,
            search_type="mmr",  # Aplicando a Estratégia 1 (MMR) aqui!
            verbose=True # Deixamos True para ver a "mágica" acontecer nos logs
        )
        # --- Fim da lógica do SelfQueryRetriever ---
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self_query_retriever, # Usamos nosso novo retriever super inteligente
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=False
        )
        print(">>> Componentes de IA com SelfQuery carregados com sucesso! <<<")

    except Exception as e:
        print(f"ERRO CRÍTICO GERAL DURANTE O CARREGAMENTO DOS COMPONENTES: {e}")
        traceback.print_exc()
        qa_chain, llm = None, None

# --- Função Principal da API ---
@functions_framework.http
def chatbot_api(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)

    if qa_chain is None:
        load_components()
        if qa_chain is None:
             print("Falha ao carregar os componentes de IA. Verifique os logs e a configuração.")
             return (jsonify({"error": "O sistema de IA falhou ao carregar. Verifique os logs da função."}), 500, headers)

    if request.method == 'POST':
        try:
            request_json = request.get_json(silent=True)
            if not request_json or 'query' not in request_json:
                return (jsonify({"error": "Pedido inválido. Forneça uma pergunta."}), 400, headers)

            query = request_json['query']

            if query.lower().strip() in ["olá", "oi", "ola", "hello", "hi"]:
                greeting_text = "Olá! Sou a assistente virtual Takwara, expert em construção sustentável com bambu. Como posso ajudar?"
                return (jsonify({"answer": greeting_text}), 200, headers)
            
            # --- LÓGICA DE CONSULTA SIMPLIFICADA E CORRIGIDA ---
            # A cadeia RetrievalQA espera um dicionário com a chave "query".
            # Ela mesma vai usar o retriever para buscar os documentos e responder.
            print(f"Invocando a cadeia de QA com a pergunta: {query}")
            result = qa_chain.invoke({"query": query})
            
            # A resposta da cadeia fica na chave "result".
            answer = result.get('result', 'Não consegui encontrar uma resposta.')
            
            print(f"Resposta gerada: {answer[:80]}...") # Loga o início da resposta
            return (jsonify({"answer": answer}), 200, headers)

        except Exception as e:
            print(f"ERRO INESPERADO DURANTE O PROCESSAMENTO DA PERGUNTA: {e}")
            traceback.print_exc()
            return (jsonify({"error": f"Ocorreu um erro interno ao processar sua pergunta."}), 500, headers)
    else:
        return (jsonify({"error": f"Método '{request.method}' não permitido."}), 405, headers)
