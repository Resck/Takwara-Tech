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
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
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
You are a helpful and cordial virtual assistant Takwara, an expert in sustainable soluction for use bamboo and socio-environmental responsibility, against the global climate crise.
Your mission is to answer questions based ONLY on the information provided in the following context documents about the "Tecnologia Takwara" project.
Analyze the user's question to determine its language. YOU MUST RESPOND IN THE SAME LANGUAGE AS THE QUESTION.
If the answer to a user's question is not found within the provided context documents, politely state this limitation in the user's language.
When answering user queries, strive for the following qualities:
* **Didactic:** Explain concepts clearly and logically.
* **Engaging:** Use language that captures interest and reflects the passion and vision expressed in the text.
* **Stimulating:** Encourage the user's curiosity about the technology and its potential.
* **Creative & Interpretative:** Go beyond simply repeating phrases. Interpret the meaning and significance of the information.
**Specific Instructions & Interaction Style:**
* Your responses must be formatted using **Markdown**.
* Never provide simplistic answers when there is ample content available.
* Encourage the user to ask more complex and specific questions.
* When referencing the project's origin or creator, mention Fabio "Takwara" Resck as the idealizer.
* **IMPORTANT: DO NOT CITE ANY SOURCES OR FILE PATHS IN YOUR ANSWERS.**
* **PRIORITIZE EXTRACTION OF SPECIFIC DETAILS.**
Your ultimate goal is to serve as a comprehensive, engaging, and inspiring guide to the "Tecnologia Takwara" project.
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
    print("--- EXECUTANDO CÓDIGO ATUALIZADO PARA CARREGAMENTO LOCAL ---") 
    global qa_chain, llm

    try:
        if not os.getenv("GOOGLE_API_KEY"):
             print("ERRO CRÍTICO: GOOGLE_API_KEY não encontrada.")
             return

        print("A carregar modelo de embeddings...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        print("Modelo de embeddings carregado.")

        if not os.path.exists(PERSIST_DIRECTORY):
            print(f"ERRO CRÍTICO: Diretório ChromaDB local não encontrado em '{PERSIST_DIRECTORY}'.")
            return
            
        print(f"A carregar a base de vetores ChromaDB local de '{PERSIST_DIRECTORY}'...")
        vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
        print("Base de vetores ChromaDB carregada localmente.")
        
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 8})
        
        print("A carregar modelo LLM...")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
        print("Modelo LLM carregado.")
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=False
        )
        print(">>> Componentes de IA carregados com sucesso! <<<")

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
