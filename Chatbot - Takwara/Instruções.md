Fase 1: O Backend (O Cérebro): Criaremos e publicaremos uma API na nuvem que recebe uma pergunta e devolve uma resposta. Este será o nosso "cérebro" reutilizável.
Fase 2: O Frontend (O Rosto): Criaremos a interface de chat com HTML, CSS e JavaScript que será hospedada no GitHub Pages. Ela vai conversar com o nosso "cérebro".
Fase 3: A Automação (A Memória): Criaremos uma GitHub Action para que o conhecimento do nosso chatbot sobre o seu repositório se mantenha sempre atualizado automaticamente.
Vamos focar totalmente na Fase 1 por agora. Ao final dela, teremos uma API funcional e pública.

Fase 1: Construir e Publicar o Backend (O Cérebro) na Nuvem
Para o nosso backend, usaremos o Google Cloud Functions, uma plataforma "serverless" (sem servidor) que é perfeita para isso e tem um excelente plano gratuito.

Passo 1: Organizar o Projeto para a API
No seu computador, vamos criar uma nova estrutura de pastas separada para a nossa API. Pode ser dentro do seu projeto Chatbot Github.

/Chatbot Github
|-- backend-api/
|   |-- main.py           # O código da nossa API
|   |-- requirements.txt  # As dependências da API
|   |-- .env.yaml         # O nosso segredo (API Key)
|   |-- create_vector_store.py  # Script para criar a base de conhecimento
|
|-- (outros arquivos como app.py, .venv, etc.)
Passo 2: Criar a Base de Conhecimento (Script Único)
Primeiro, precisamos de um script que leia o seu repositório e salve a base de dados de vetores no disco. Isso só será executado uma vez por nós para começar, e depois será automatizado na Fase 3.

Crie o arquivo backend-api/create_vector_store.py:

Python

# backend-api/create_vector_store.py
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import GitLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# URL do repositório que você quer que o chatbot conheça
REPO_URL = "https://github.com/Resck/Takwara-Tech" 
# Pasta onde a base de vetores será salva
PERSIST_DIRECTORY = "./chroma_db"

def build_and_save_vector_store():
    print("Iniciando o clone do repositório...")
    loader = GitLoader(
        clone_url=REPO_URL,
        repo_path="./temp_repo",
        file_filter=lambda file_path: file_path.endswith((".py", ".md", ".txt"))
    )
    docs = loader.load()
    
    if not docs:
        print("Nenhum documento encontrado. Verifique o repositório e o filtro.")
        return

    print(f"{len(docs)} documentos encontrados. Dividindo os textos...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    print("Gerando embeddings e criando a base de vetores Chroma...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Cria e salva a base de dados no disco
    vector_store = Chroma.from_documents(
        documents=split_docs, 
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY 
    )
    
    print(f"Base de vetores criada e salva com sucesso em '{PERSIST_DIRECTORY}'!")

if __name__ == "__main__":
    build_and_save_vector_store()

Para executar este script:

Navegue no terminal para a pasta backend-api.
Instale as dependências: pip install python-dotenv langchain-community langchain-google-genai GitPython chromadb.
Execute: python create_vector_store.py.
Ao final, você terá uma nova pasta backend-api/chroma_db cheia de arquivos. Essa é a "memória" do seu chatbot!

Passo 3: Codificar a API (main.py)
Agora, vamos criar o código da API que irá ler essa base de dados e responder perguntas.

Crie o arquivo backend-api/main.py:

Python

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
    # Configura CORS para permitir requisições do GitHub Pages
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    if request.method == 'OPTIONS':
        return '', 204, headers

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

Passo 4: Preparar as Dependências e Segredos
Crie o arquivo backend-api/requirements.txt:
Plaintext

functions-framework==3.*
flask==3.*
langchain-community==0.2.5
langchain-google-genai==1.0.6
langchain-core==0.2.9
langchain==0.2.5
chromadb==0.5.3
GitPython # Necessário pelo Chroma para algumas operações
Crie o arquivo backend-api/.env.yaml para guardar sua chave de API de forma segura na nuvem:
YAML

GOOGLE_API_KEY: 'SUA_CHAVE_API_AQUI' 
Passo 5: Configurar o Google Cloud e Fazer o Deploy
Esta é a parte mais técnica, mas siga com atenção.

Crie uma Conta e Projeto: Se ainda não tiver, crie uma conta no Google Cloud e crie um novo projeto (ex: meu-chatbot-github).

Ative as APIs: No seu projeto no Google Cloud, vá em "APIs e Serviços" e ative a "Cloud Functions API" e a "Cloud Build API".

Instale o gcloud CLI: Siga o guia de instalação para instalar a ferramenta de linha de comando gcloud na sua máquina. Depois de instalar, autentique-se com gcloud auth login.

Faça o Deploy! Navegue com o seu terminal até a pasta backend-api. Certifique-se de que a pasta chroma_db está lá dentro. Então, execute o comando de deploy:

Bash

gcloud functions deploy chatbot-api \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=chatbot_api \
  --trigger-http \
  --allow-unauthenticated \
  --env-vars-file=.env.yaml
Este comando irá empacotar todo o conteúdo da pasta backend-api (incluindo a chroma_db), enviá-lo para o Google Cloud e publicar a sua API. Pode demorar alguns minutos.

Passo 6: Testar a API
Ao final do deploy, o terminal mostrará um URL do acionador (Trigger URL). Será algo como https://us-central1-seu-projeto.cloudfunctions.net/chatbot-api.

Você pode testá-la usando um programa como o Postman ou o comando curl no terminal:

Bash

curl -X POST "SEU_TRIGGER_URL_AQUI" \
-H "Content-Type: application/json" \
-d '{"question": "Qual o objetivo do arquivo auxiliar.py?"}'
Se tudo correu bem, você receberá de volta um JSON com a resposta do chatbot!

Parabéns! Ao final desta fase, você terá um "cérebro" de chatbot funcional, publicado na internet e pronto para ser consumido. Esta é a parte mais difícil.

