# main.py - Versão de DEPURAÇÃO DE CAMINHOS
import os
import functions_framework
from flask import jsonify

# --- CÓDIGO DETETIVE DE CAMINHOS ---
# Este bloco irá imprimir nos logs a estrutura de arquivos que a aplicação encontra.
print("--- [DETETIVE] INICIANDO VERIFICAÇÃO DE CAMINHOS ---")
try:
    cwd_path = os.getcwd()
    print(f"--- [DETETIVE] Diretório de trabalho atual (CWD): {cwd_path}")
    print(f"--- [DETETIVE] Conteúdo do CWD: {os.listdir(cwd_path)}")

    # Onde esperamos que a base de dados esteja
    db_path = os.path.join(cwd_path, 'chroma_db')
    print(f"--- [DETETIVE] Verificando a existência do caminho: {db_path}")
    if os.path.exists(db_path):
        print("--- [DETETIVE] SUCESSO! A pasta 'chroma_db' foi encontrada!")
        print(f"--- [DETETIVE] Conteúdo da 'chroma_db': {os.listdir(db_path)}")
    else:
        print("--- [DETETIVE] FALHA! A pasta 'chroma_db' NÃO foi encontrada no diretório de trabalho atual.")
except Exception as e:
    print(f"--- [DETETIVE] Ocorreu um erro ao verificar os caminhos: {e}")
print("--- [DETETIVE] FIM DA VERIFICAÇÃO DE CAMINHOS ---")
# --- FIM DO CÓDIGO DETETIVE ---


# O nosso código original da IA começa aqui.
# Note que ele irá falhar se o ChromaDB não for encontrado, e isso é o que queremos testar.
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

PERSIST_DIRECTORY = "./chroma_db"
EMBEDDING_MODEL = "models/embedding-001"
LLM_MODEL = "gemini-1.5-flash"

embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.3)
# ... (O resto do seu código completo continua aqui, sem alterações)
# (Copie e cole o resto do seu main.py inteligente a partir desta linha)
retriever = vector_store.as_retriever()

qa_prompt_template = ChatPromptTemplate.from_template("""
Responda à pergunta do utilizador de forma clara e concisa, com base apenas no contexto fornecido.
Se a resposta não estiver no contexto, diga: "Não encontrei informações sobre isso no repositório."

Contexto:
{context}

Pergunta:
{input}
""")
qa_document_chain = create_stuff_documents_chain(llm, qa_prompt_template)
retrieval_chain = create_retrieval_chain(retriever, qa_document_chain)

# O CÓDIGO CORRIGIDO
social_prompt_template = ChatPromptTemplate.from_template("""
Você é o assistente cordial do projeto Tecnologia Takwara. Responda de forma amigável e direta.
Não se apresente a menos que perguntem.
Se o utilizador agradecer, agradeça de volta.
Se o utilizador fizer uma saudação, responda à saudação.
O contexto abaixo é para perguntas técnicas e pode estar vazio para conversas casuais.

Contexto:
{context}

Pergunta do Utilizador:
{input}
""")

social_chain = create_stuff_documents_chain(llm, social_prompt_template)

@functions_framework.http
def chatbot_api(request):
    headers = {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Methods': 'POST, OPTIONS','Access-Control-Allow-Headers': 'Content-Type',}
    if request.method == 'OPTIONS':
        return '', 204, headers
    if request.method == 'POST':
        request_json = request.get_json(silent=True)
        user_question = request_json.get('question', '').lower() if request_json else ""
        if not user_question:
            return jsonify({"error": "'question' ausente."}), 400, headers

        greetings = ["olá", "oi", "bom dia", "boa tarde", "boa noite", "tudo bem", "como vai"]
        thanks = ["obrigado", "obrigada", "valeu", "agradecido", "agradecida", "grato", "grata"]

        if any(word in user_question for word in greetings) or any(word in user_question for word in thanks):
            response = social_chain.invoke({"input": user_question, "context": []})
        else:
            response = retrieval_chain.invoke({"input": user_question})

        return jsonify({"answer": response.get("answer", "Ocorreu um erro.")}), 200, headers
    return jsonify({"error": "Método não permitido."}), 405, headers