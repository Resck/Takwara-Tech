# O código da nossa API
# backend-api/main.py
import os
import functions_framework
from flask import jsonify
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Constantes
PERSIST_DIRECTORY = "./chroma_db"
EMBEDDING_MODEL = "models/embedding-001"
LLM_MODEL = "gemini-1.5-flash"

# Carrega a base de vetores e o LLM uma vez quando a função é iniciada
# Isto otimiza o tempo de resposta, pois não recarrega a cada chamada.
embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.3)
retriever = vector_store.as_retriever()

prompt_template = ChatPromptTemplate.from_template("""
Responda à pergunta do utilizador de forma clara e concisa, com base apenas no contexto fornecido.
Se a resposta não estiver no contexto, diga educadamente: "Não encontrei informações sobre isso no repositório."

Contexto:
{context}

Pergunta:
{input}
""")

document_chain = create_stuff_documents_chain(llm, prompt_template)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

@functions_framework.http
def chatbot_api(request):
    """
    Função HTTP Cloud que recebe uma pergunta e retorna a resposta do chatbot.
    """
    # Configura CORS para permitir requisições de qualquer origem (ex: GitHub Pages)
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    # Responde a requisições preflight do browser
    if request.method == 'OPTIONS':
        return '', 204, headers

    # Processa a requisição principal
    if request.method == 'POST':
        request_json = request.get_json(silent=True)
        if request_json and 'question' in request_json:
            user_question = request_json['question']
            
            response = retrieval_chain.invoke({"input": user_question})
            answer = response.get("answer", "Ocorreu um erro ao processar a resposta.")
            
            return jsonify({"answer": answer}), 200, headers
        else:
            return jsonify({"error": "JSON inválido ou 'question' ausente."}), 400, headers
            
    return jsonify({"error": "Método não permitido."}), 405, headers