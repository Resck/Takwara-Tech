# /Users/fabiotakwara/Documents/GitHub/Takwara-Tech/Chatbot - Takwara/backend-api/main.py
# VERSÃO FINAL, CORRIGIDA E COMPLETA

import os
import functions_framework
from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever

load_dotenv()
app = Flask(__name__)

# A cadeia de IA começa como 'None' e só será carregada no primeiro pedido.
qa_chain = None
vector_store = None # Também definimos o vector_store globalmente

def load_qa_chain():
    """Carrega a cadeia de IA com um retriever avançado (MultiQuery)."""
    global qa_chain, vector_store
    print("Iniciando o carregamento da base de vetores e do modelo...")
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        persist_directory = "./chroma_db"
        vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)

        prompt_template = """
        You are a helpful and cordial virtual assistant for Takwara-Tech, an expert in sustainable construction with bamboo.
        Your mission is to answer questions based ONLY on the information provided in the following context documents.
        Analyze the user's question to determine its language. YOU MUST RESPOND IN THE SAME LANGUAGE AS THE QUESTION.
        If the user's question has spelling or grammatical errors, interpret it to the best of your ability and answer the most likely intended question.
        If the answer is not in the documents, politely say so in the user's language.
        At the end of your answer, if possible, cite the source document from where you extracted the information.

        Context (Documents):
        {context}

        Question:
        {question}

        Helpful and cordial answer in the user's language:
        """
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        # --- UPGRADE DO RETRIEVER com PARÂMETROS AVANÇADOS ---
        print("A criar um MultiQueryRetriever com parâmetros de busca avançados...")

        # Criamos o retriever base com novas instruções:
        base_retriever = vector_store.as_retriever(
            search_type="mmr",  # Usa o método 'Maximal Marginal Relevance' para diversificar os resultados
            search_kwargs={"k": 6} # Pede para ele encontrar os 6 documentos mais relevantes
        )

        # Criamos o MultiQuery a partir do nosso retriever base afinado
        retriever_from_llm = MultiQueryRetriever.from_llm(
            retriever=base_retriever, 
            llm=llm
        )
        # --- FIM DO UPGRADE ---

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever_from_llm,
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        print(">>> Modelo e base de vetores carregados com o MultiQueryRetriever! <<<")
    except Exception as e:
        print(f"ERRO CRÍTICO AO CARREGAR O MODELO: {e}")
        qa_chain = None

# def load_qa_chain():
#     """Carrega a cadeia de IA com um retriever avançado (MultiQuery)."""
#     global qa_chain, vector_store
#     print("Iniciando o carregamento da base de vetores e do modelo...")
#     try:
#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#         persist_directory = "./chroma_db"
#         vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
#         llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)

#         # Prompt corrigido, sem o texto extra em português.
#         prompt_template = """
# You are a helpful and cordial virtual assistant for Takwara-Tech, an expert in sustainable construction with bamboo.
# Your mission is to answer questions based ONLY on the information provided in the following context documents.
# Analyze the user's question to determine its language. YOU MUST RESPOND IN THE SAME LANGUAGE AS THE QUESTION.
# If the user's question has spelling or grammatical errors, interpret it to the best of your ability and answer the most likely intended question.
# If the answer is not in the documents, politely say so in the user's language.
# At the end of your answer, if possible, cite the source document from where you extracted the information.

# Context (Documents):
# {context}

# Question:
# {question}

# Helpful and cordial answer in the user's language:
# """
#         PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

#         print("A criar um MultiQueryRetriever para buscas mais inteligentes...")
#         retriever_from_llm = MultiQueryRetriever.from_llm(
#             retriever=vector_store.as_retriever(), 
#             llm=llm
#         )

#         qa_chain = RetrievalQA.from_chain_type(
#             llm=llm,
#             chain_type="stuff",
#             retriever=retriever_from_llm,
#             chain_type_kwargs={"prompt": PROMPT},
#             return_source_documents=True
#         )
#         print(">>> Modelo e base de vetores carregados com o MultiQueryRetriever! <<<")
#     except Exception as e:
#         print(f"ERRO CRÍTICO AO CARREGAR O MODELO: {e}")
#         qa_chain = None

@functions_framework.http
def chatbot_api(request):
    global qa_chain, vector_store
    
    if qa_chain is None:
        load_qa_chain()

    if qa_chain is None:
        return (jsonify({"error": "O modelo de IA falhou ao carregar. Verifique os logs do servidor."}), 500, {'Access-Control-Allow-Origin': '*'})

    headers = {'Access-Control-Allow-Origin': '*'}
    if request.method == 'OPTIONS':
        response = make_response('', 204)
        headers.update({'Access-Control-Allow-Methods': 'POST, GET, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type'})
        response.headers.extend(headers)
        return response

    request_json = request.get_json(silent=True)
    
    if request_json and 'query' in request_json:
        query = request_json['query']
        context_url = request_json.get('context')
        
        if query.lower().strip() in ["olá", "oi", "ola"]:
            return (jsonify({"answer": "Olá, eu sou a assistente virtual Takwara. Em que posso ajudar?"}), 200, headers)
            
        try:
            retriever = qa_chain.retriever
            source_file = None
            if context_url and context_url != "/" and context_url != "/chatbot/":
                try:
                    source_file = os.path.basename(context_url.strip('/')).replace('%20', ' ') + ".md"
                    print(f"Contexto identificado. A procurar primeiro em: {source_file}")
                    # Cria um retriever específico para o ficheiro de contexto
                    retriever = vector_store.as_retriever(
                        search_kwargs={'filter': {'source': source_file}}
                    )
                except:
                    pass
            
            print(f"A procurar documentos para a pergunta: '{query}'")
            retrieved_docs = retriever.get_relevant_documents(query)
            
            if not retrieved_docs and source_file:
                print(f"Nenhum documento encontrado no contexto '{source_file}'. A fazer busca geral.")
                retrieved_docs = qa_chain.retriever.get_relevant_documents(query)

            result = qa_chain.combine_documents_chain.invoke({
                "input_documents": retrieved_docs,
                "question": query
            })
            
            answer = result.get('output_text', 'Não foi possível extrair uma resposta.')
            sources = [doc.metadata.get('source', 'desconhecida') for doc in retrieved_docs]
            unique_sources = list(set(sources))
            
            if unique_sources:
                answer += f"\n\nFonte(s): {', '.join(unique_sources)}"

            return (jsonify({"answer": answer}), 200, headers)

        except Exception as e:
            return (jsonify({"error": f"Erro ao processar a sua pergunta: {str(e)}"}), 500, headers)
    else:
        return (jsonify({"error": "Pedido inválido."}), 400, headers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)