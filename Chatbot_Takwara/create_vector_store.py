# -*- coding: utf-8 -*-
"""
VERSÃO 5.1: Adiciona Metadados e usa caminhos inteligentes para ser executado de qualquer lugar.
- Etiqueta cada documento como 'publico' (.md) ou 'privado' (.pdf).
"""
import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import traceback

# --- CÓDIGO INTELIGENTE PARA ENCONTRAR OS CAMINHOS CORRETOS ---
# Encontra o diretório do script (ex: .../Takwara-Tech/Chatbot_Takwara)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Sobe um nível para encontrar a raiz do projeto (ex: .../Takwara-Tech)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# --- FIM DO CÓDIGO ---

load_dotenv()

# --- Configurações com Caminhos Corrigidos ---
PUBLIC_DOCS_FOLDER = os.path.join(PROJECT_ROOT, 'docs')
PRIVATE_DOCS_FOLDER = os.path.join(SCRIPT_DIR, 'fontes-privadas')
PERSIST_DIRECTORY = os.path.join(SCRIPT_DIR, 'backend-api', 'chroma_db')
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

def build_and_save_vector_store():
    print("--- INICIANDO CRIAÇÃO DA BASE (v5.1 - Com Caminhos Inteligentes) ---")
    
    all_docs = []

    # Carrega docs públicos e adiciona metadado
    if os.path.isdir(PUBLIC_DOCS_FOLDER):
        print(f"-> Lendo documentos públicos de: '{PUBLIC_DOCS_FOLDER}'")
        loader_public = DirectoryLoader(PUBLIC_DOCS_FOLDER, glob="**/*.md", loader_cls=TextLoader, recursive=True, show_progress=True)
        public_docs = loader_public.load()
        for doc in public_docs:
            doc.metadata["source_type"] = "publico"
        all_docs.extend(public_docs)
        print(f"-> Carregados e etiquetados {len(public_docs)} documentos públicos.")
    else:
        print(f"AVISO: Diretório público não encontrado em '{PUBLIC_DOCS_FOLDER}'. Pulando.")

    # Carrega docs privados e adiciona metadado
    if os.path.isdir(PRIVATE_DOCS_FOLDER):
        print(f"-> Lendo documentos privados de: '{PRIVATE_DOCS_FOLDER}'")
        loader_private = DirectoryLoader(PRIVATE_DOCS_FOLDER, glob="**/*.pdf", loader_cls=PyMuPDFLoader, recursive=True, show_progress=True, silent_errors=True)
        private_docs = loader_private.load()
        for doc in private_docs:
            doc.metadata["source_type"] = "privado"
        all_docs.extend(private_docs)
        print(f"-> Carregados e etiquetados {len(private_docs)} documentos privados.")
    else:
        print(f"AVISO: Diretório privado não encontrado em '{PRIVATE_DOCS_FOLDER}'. Pulando.")

    if not all_docs:
        print("\nERRO: Nenhum documento foi encontrado para processar. Verifique os caminhos e o conteúdo das pastas.")
        return
    
    print("\n[ETAPA 2/3] Dividindo todos os documentos em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(all_docs)
    print(f"-> Divisão concluída. Total de chunks gerados: {len(chunks)}")

    print(f"\n[ETAPA 3/3] Gerando embeddings e salvando a base com metadados...")
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        if os.path.exists(PERSIST_DIRECTORY):
            shutil.rmtree(PERSIST_DIRECTORY)
            print("-> Base de dados antiga removida.")
            
        Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=PERSIST_DIRECTORY)
        print(f"\n--- SUCESSO! Nova base de vetores com metadados criada em '{PERSIST_DIRECTORY}'! ---")
    except Exception as e:
        print(f"\nERRO FATAL: {e}")
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    build_and_save_vector_store()