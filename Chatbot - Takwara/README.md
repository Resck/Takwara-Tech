Guia Completo: Como Criar um Chatbot Inteligente para o seu Repositório no GitHub
Bem-vindo, desenvolvedor e inovador! Este guia é um passo a passo detalhado para construir uma aplicação web completa: um chatbot inteligente capaz de responder a perguntas sobre o conteúdo de qualquer repositório no GitHub.

Ao final desta jornada, você terá:

Um backend (o "cérebro") publicado na nuvem, usando Python, LangChain e a API da Google.
Um frontend (o "rosto") bonito e interativo, publicado gratuitamente no GitHub Pages.
Vamos começar.

Fase 1: Construindo o "Cérebro" (O Backend Serverless)
Nesta fase, construiremos a API que lê um repositório, cria uma base de conhecimento e responde a perguntas.

Passo 1.1: Estrutura de Pastas
No seu projeto, crie uma pasta para o backend para manter tudo organizado.

    /Seu-Projeto/
|-- backend-api/
|   |-- .env
|   |-- create_vector_store.py
|   |-- main.py
|   |-- requirements.txt
|
|-- .venv/
|-- README.md

Passo 1.2: O Script de Criação da Base de Conhecimento
Este script é o coração do nosso sistema de conhecimento. Ele clona o repositório, divide os textos e os transforma em vetores numéricos que a IA entende, salvando tudo numa base de dados local.

Crie o arquivo backend-api/create_vector_store.py:

Python

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import GitLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

REPO_URL = "URL_DO_SEU_REPOSITORIO_AQUI" # Ex: "https://github.com/Resck/Takwara-Tech"
PERSIST_DIRECTORY = "./chroma_db"

def build_and_save_vector_store():
    print("--- O SCRIPT COMEÇOU A SER EXECUTADO ---")
    print(f"A clonar o repositório: {REPO_URL}")
    
    loader = GitLoader(
        clone_url=REPO_URL,
        repo_path="./temp_repo",
        file_filter=lambda file_path: file_path.endswith((".py", ".md", ".txt"))
    )
    
    print("A carregar os documentos...")
    docs = loader.load()
    
    if not docs:
        print("AVISO: Nenhum documento .py, .md ou .txt foi encontrado.")
        return

    print(f"Sucesso! {len(docs)} documentos encontrados. A dividir os textos...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    print("A gerar os embeddings e a criar a base de vetores. Isto pode demorar...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    vector_store = Chroma.from_documents(
        documents=split_docs, 
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print(f"--- SUCESSO! Base de vetores criada e salva em '{PERSIST_DIRECTORY}'! ---")

if __name__ == "__main__":
    build_and_save_vector_store()

    ++++++++++++++++++++

  Passo 1.3: O Código da API
Este script será a nossa API na nuvem. Ele carrega a base de conhecimento já criada e usa-a para responder a perguntas.

Crie o arquivo backend-api/main.py:

Python

import os
import functions_framework
from flask import jsonify
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

PERSIST_DIRECTORY = "./chroma_db"
EMBEDDING_MODEL = "models/embedding-001"
LLM_MODEL = "gemini-1.5-flash"

embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.3)
retriever = vector_store.as_retriever()

prompt_template = ChatPromptTemplate.from_template("""
Responda à pergunta do utilizador de forma clara e concisa, com base apenas no contexto fornecido.
Se a resposta não estiver no contexto, diga: "Não encontrei informações sobre isso no repositório."

Contexto:
{context}

Pergunta:
{input}
""")

document_chain = create_stuff_documents_chain(llm, prompt_template)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

@functions_framework.http
def chatbot_api(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    if request.method == 'OPTIONS':
        return '', 204, headers

    if request.method == 'POST':
        request_json = request.get_json(silent=True)
        user_question = request_json.get('question') if request_json else None
        if user_question:
            response = retrieval_chain.invoke({"input": user_question})
            return jsonify({"answer": response.get("answer", "Erro.")}), 200, headers
        else:
            return jsonify({"error": "JSON inválido ou 'question' ausente."}), 400, headers
            
    return jsonify({"error": "Método não permitido."}), 405, headers
Passo 1.4: Configuração do Ambiente Local e Instalação
Esta é a fase com mais armadilhas. Vamos navegar por elas juntos.

Crie e Ative um Ambiente Virtual com Python 3.11:

Navegue para a pasta principal do seu projeto.
Execute: python3.11 -m venv .venv
Ative-o: source .venv/bin/activate
Verifique: python --version (a saída deve ser Python 3.11.x)
Prepare a "Lista de Compras" (requirements.txt):
Dentro de backend-api, crie o arquivo requirements.txt com versões específicas para evitar problemas.

Plaintext

functions-framework==3.8.3
flask==3.0.3
gunicorn==22.0.0
langchain-community==0.2.5
langchain-google-genai==1.0.6
langchain==0.2.5
chromadb==0.5.3
GitPython==3.1.43
python-dotenv==1.0.1
Instale as Dependências (O Método Robusto):

Navegue para a pasta backend-api.
Execute: python -m pip install -r requirements.txt
Solução de Erros Comuns na Instalação:

Erro: ModuleNotFoundError: No module named 'X'
Causa: O pacote 'X' não está instalado no seu ambiente.
Solução: Certifique-se de que o seu requirements.txt está completo e execute python -m pip install -r requirements.txt novamente. O comando python -m pip garante que você está a usar o pip correto para o seu ambiente python ativo.
Erro: A instalação demora uma eternidade ou trava.
Causa: Você não especificou as versões no requirements.txt, e o pip está a testar centenas de combinações.
Solução: Use a lista com versões específicas (como a que fornecemos acima) para dar ao pip um "mapa" exato do que instalar.
Erro: No matching distribution found for onnxruntime
Causa: A sua versão do Python (ex: 3.12, 3.13) é muito recente e pacotes essenciais ainda não são compatíveis.
Solução: Crie um novo ambiente virtual usando uma versão estável como a 3.11 (python3.11 -m venv .venv), que é compatível com todas as nossas dependências.
Passo 1.5: Execução Local e Deploy na Nuvem
Crie o Arquivo .env Local:

Dentro de backend-api, crie um arquivo .env.
Adicione a sua chave: GOOGLE_API_KEY=SUA_CHAVE_AQUI
Execute o Script de Criação:

No terminal, na pasta backend-api, execute: python create_vector_store.py.
Verifique se a pasta chroma_db foi criada.
Solução de Erros Comuns na Execução:

Erro: Did not find google_api_key...
Causa: O script create_vector_store.py precisa da sua chave de API para gerar os embeddings, mas não a encontrou.
Solução: Certifique-se de que o arquivo .env foi criado na pasta backend-api com o conteúdo correto.
Faça o Deploy para o Google Cloud:
Instale a CLI gcloud e faça login (gcloud auth login).
Configure o seu projeto: gcloud config set project SEU_ID_DE_PROJETO
Execute o comando de deploy de dentro da pasta backend-api:
Bash

gcloud functions deploy chatbot-api \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=chatbot_api \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=SUA_CHAVE_AQUI"
Solução de Erros Comuns no Deploy:

Erro: gcloud: command not found
Causa: Você está a usar uma janela de terminal que foi aberta antes da instalação da gcloud terminar.
Solução: Feche completamente o seu terminal e abra um novo.
Erro: Container Healthcheck Failed
Causa: Faltou o servidor web gunicorn para gerir a aplicação na nuvem.
Solução: Adicione gunicorn ao seu requirements.txt e faça o deploy novamente.
Teste a API:
Após o deploy, pegue o URL fornecido e teste com o comando curl:
Bash

curl -X POST "SEU_URL_DA_API_AQUI" \
-H "Content-Type: application/json" \
-d '{"question": "Qualquer pergunta sobre seu repositório?"}'
Fase 2: Construindo o "Rosto" (O Frontend no GitHub Pages)
Com o cérebro no ar, vamos criar a interface.

Crie os Arquivos: Numa pasta frontend/, crie os arquivos index.html, style.css e script.js com o conteúdo que discutimos anteriormente.

Conecte o Frontend ao Backend:

No arquivo script.js, encontre a linha const apiUrl = '...';
Substitua o conteúdo pelo URL da sua API que você obteve no final da Fase 1.
Publique no GitHub Pages:

Envie a pasta frontend/ para o seu repositório no GitHub.
Nas configurações (Settings) do seu repositório, vá para a seção "Pages".
Selecione "Deploy from a branch".
Escolha a sua branch (main) e a pasta /frontend como a fonte.
Salve e aguarde alguns minutos. O seu site com o chatbot estará no ar!
Conclusão

Parabéns! Seguindo estes passos, você construiu uma aplicação de IA completa e robusta. Você navegou por desafios de ambiente, dependências, configuração de nuvem e integração de frontend/backend. Esperamos que este guia ajude muitos outros a transformar as suas ideias em realidade.  

    