# /Users/fabiotakwara/Documents/GitHub/Takwara-Tech/Chatbot - Takwara/backend-api/main.py
# VERSÃO DE DEBUGGING CORRIGIDA E COMPLETA

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

qa_chain = None

def load_qa_chain():
    """Carrega a cadeia de IA com um retriever avançado (MultiQuery)."""
    global qa_chain
    print("Iniciando o carregamento da base de vetores e do modelo...")
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        persist_directory = "./chroma_db"
        vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)

        prompt_template = """
        Você é a assistente virtual da Takwara-Tech, uma especialista em construção sustentável com bambu.
        Sua missão é ser cordial, prestativa e responder às perguntas usando apenas as informações fornecidas nos seguintes documentos.
        Seja clara e responda em Português do Brasil.
        Se a resposta não estiver nos documentos, diga educadamente que não possui essa informação.
        Ao final da sua resposta, se possível, cite o nome do documento de onde extraiu a informação.

        Contexto (Documentos):
        {context}

        Pergunta:
        {question}

        Resposta útil e cordial:
        """
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        # --- UPGRADE DO RETRIEVER ---
        print("A criar um MultiQueryRetriever para buscas mais inteligentes...")
        retriever_from_llm = MultiQueryRetriever.from_llm(
            retriever=vector_store.as_retriever(), 
            llm=llm
        )
        # --- FIM DO UPGRADE ---

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever_from_llm, # <--- Usamos o nosso novo retriever avançado
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        print(">>> Modelo e base de vetores carregados com o MultiQueryRetriever! <<<")
    except Exception as e:
        print(f"ERRO CRÍTICO AO CARREGAR O MODELO: {e}")
        qa_chain = None

@functions_framework.http
def chatbot_api(request):
    global qa_chain
    
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
        
        if query.lower().strip() in ["olá", "oi", "ola"]:
            return (jsonify({"answer": "Olá, eu sou a assistente virtual Takwara. Em que posso ajudar?"}), 200, headers)
            
        # O bloco try...except começa aqui, alinhado com o 'if' acima
        try:
            source_file = None
            context_url = request_json.get('context')
            if context_url and context_url != "/" and context_url != "/chatbot/":
                try:
                    source_file = os.path.basename(context_url.strip('/')).replace('%20', ' ') + ".md"
                    print(f"Contexto identificado. A procurar primeiro em: {source_file}")
                except:
                    source_file = None
            
            retriever = qa_chain.retriever
            if source_file:
                retriever = vector_store.as_retriever(
                    search_kwargs={'filter': {'source': source_file}}
                )
            
            print(f"A procurar documentos para a pergunta: '{query}'")
            retrieved_docs = retriever.get_relevant_documents(query)
            
            if not retrieved_docs:
                print(f"Nenhum documento encontrado no contexto. A fazer busca geral.")
                retrieved_docs = qa_chain.retriever.get_relevant_documents(query)

            print(f"--- BUSCA CONCLUÍDA. {len(retrieved_docs)} DOCUMENTOS ENCONTRADOS ---")

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
            print(f"!!! ERRO DURANTE A EXECUÇÃO DA IA: {e} !!!")
            return (jsonify({"error": f"Erro ao processar a sua pergunta: {str(e)}"}), 500, headers)
    else:
        return (jsonify({"error": "Pedido inválido."}), 400, headers)