# -*- coding: utf-8 -*-
"""
VERSÃO 5.0: Adiciona Metadados para Busca Inteligente (SelfQuery).
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

load_dotenv()

PUBLIC_DOCS_FOLDER = './docs'
PRIVATE_DOCS_FOLDER = './fontes-privadas'
PERSIST_DIRECTORY = './backend-api/chroma_db'
CHUNK_SIZE = 800  # Mantendo chunks menores para melhor precisão
CHUNK_OVERLAP = 150

def build_and_save_vector_store():
    print("--- INICIANDO CRIAÇÃO DA BASE (v5.0 - Com Metadados) ---")
    
    # Carrega docs públicos e adiciona metadado
    print(f"-> Lendo documentos públicos de: '{PUBLIC_DOCS_FOLDER}'")
    loader_public = DirectoryLoader(PUBLIC_DOCS_FOLDER, glob="**/*.md", loader_cls=TextLoader, recursive=True, show_progress=True)
    public_docs = loader_public.load()
    for doc in public_docs:
        doc.metadata["source_type"] = "publico"
    print(f"Carregados e etiquetados {len(public_docs)} documentos públicos.")

    # Carrega docs privados e adiciona metadado
    print(f"-> Lendo documentos privados de: '{PRIVATE_DOCS_FOLDER}'")
    loader_private = DirectoryLoader(PRIVATE_DOCS_FOLDER, glob="**/*.pdf", loader_cls=PyMuPDFLoader, recursive=True, show_progress=True, silent_errors=True)
    private_docs = loader_private.load()
    for doc in private_docs:
        doc.metadata["source_type"] = "privado"
    print(f"Carregados e etiquetados {len(private_docs)} documentos privados.")
    
    all_docs = public_docs + private_docs
    
    print("\n[ETAPA 2/3] Dividindo todos os documentos em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(all_docs)
    print(f"Divisão concluída. Total de chunks gerados: {len(chunks)}")

    print(f"\n[ETAPA 3/3] Gerando embeddings e salvando a base com metadados...")
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        if os.path.exists(PERSIST_DIRECTORY):
            shutil.rmtree(PERSIST_DIRECTORY)
        Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=PERSIST_DIRECTORY)
        print(f"\n--- SUCESSO! Nova base de vetores com metadados criada! ---")
    except Exception as e:
        print(f"\nERRO FATAL: {e}")
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    build_and_save_vector_store()