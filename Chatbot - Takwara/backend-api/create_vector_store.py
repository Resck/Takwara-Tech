# Script para criar a base de conhecimento
# backend-api/create_vector_store.py
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import GitLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Carrega variáveis de ambiente (necessário para a chave da API do Google)
load_dotenv()

# URL do repositório que você quer que o chatbot conheça
REPO_URL = "https://github.com/Resck/Takwara-Tech"
# Pasta onde a base de vetores será salva
PERSIST_DIRECTORY = "./chroma_db"

def build_and_save_vector_store():
    """
    Função principal que clona o repositório, processa os arquivos
    e salva a base de dados de vetores no disco.
    """
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
        print("AVISO: Nenhum documento .py, .md ou .txt foi encontrado no repositório. A base de dados ficará vazia.")
        return

    print(f"Sucesso! {len(docs)} documentos encontrados. A dividir os textos em pedaços...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    print("A gerar os embeddings e a criar a base de vetores Chroma. Isto pode demorar um pouco...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Cria e salva a base de dados no disco
    vector_store = Chroma.from_documents(
        documents=split_docs, 
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print(f"--- SUCESSO! Base de vetores criada e salva em '{PERSIST_DIRECTORY}'! ---")

# Esta linha garante que a função acima seja executada quando o script é chamado
if __name__ == "__main__":
    build_and_save_vector_store()