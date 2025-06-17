# /Users/fabiotakwara/Documents/GitHub/Takwara-Tech/Chatbot - Takwara/backend-api/create_vector_store.py
# --- VERSÃO OTIMIZADA COM SPLITTER INTELIGENTE PARA MARKDOWN ---

import os
import shutil
from git import Repo
from glob import glob
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
# Importamos os novos splitters
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from glob import glob

# Carrega variáveis de ambiente (necessário para a chave da API do Google)
load_dotenv()

# --- INÍCIO DO TESTE DE DIAGNÓSTICO ---
print("--- INÍCIO DO TESTE DE DIAGNÓSTICO ---")
# Tentamos ler a variável de ambiente que deveria ter sido carregada
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    # Se encontrou, mostramos apenas o início e o fim para confirmar, sem expor a chave inteira.
    print(f"SUCESSO: Chave de API encontrada! A chave começa com: '{api_key[:5]}...' e termina com: '...{api_key[-5:]}'")
else:
    # Se não encontrou, mostramos uma mensagem de erro clara.
    print("FALHA: A chave de API 'GOOGLE_API_KEY' NÃO foi encontrada no ambiente.")
    print(f"Verifique se o ficheiro .env está na pasta correta ({os.getcwd()}) e se a variável está bem escrita.")
print("--- FIM DO TESTE DE DIAGNÓSTICO ---")
# --- FIM DO TESTE ---


# --- Configurações Principais ---
REPO_URL = "https://github.com/Resck/Takwara-Tech"
REPO_PATH = "./temp_repo"
PERSIST_DIRECTORY = "./chroma_db"

def build_and_save_vector_store():
    """
    Clona/atualiza o repositório, processa os ficheiros Markdown de forma inteligente,
    e salva a base de dados de vetores no disco.
    """
    print("--- O SCRIPT OTIMIZADO COMEÇOU A SER EXECUTADO ---")

    # --- ETAPA 1: Clonar ou atualizar o repositório (lógica mantida) ---
    print(f"A garantir que o repositório '{REPO_URL}' está atualizado em '{REPO_PATH}'...")
    if os.path.exists(REPO_PATH):
        try:
            repo = Repo(REPO_PATH)
            origin = repo.remotes.origin
            origin.pull()
            print("Repositório existente atualizado com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar o repositório: {e}. A recomeçar do zero.")
            shutil.rmtree(REPO_PATH)
            Repo.clone_from(REPO_URL, REPO_PATH)
    else:
        Repo.clone_from(REPO_URL, REPO_PATH)
        print(f"Repositório clonado com sucesso de {REPO_URL}.")

    # --- ETAPA 2: Carregar e Dividir os Documentos de Forma Inteligente ---
    print("\nA carregar e a dividir todos os documentos .md da pasta 'docs'...")
    
    docs_folder_path = os.path.join(REPO_PATH, 'Chatbot - Takwara', 'docs')
    markdown_files = glob(os.path.join(docs_folder_path, '**', '*.md'), recursive=True)
    
    all_split_docs = []
    
    # Define os cabeçalhos que serão usados para dividir os documentos.
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    
    # Cria o splitter de Markdown.
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    # Cria um splitter secundário para pedaços que ainda são muito grandes.
    chunk_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for md_path in markdown_files:
        print(f"  -> Processando: {os.path.relpath(md_path, REPO_PATH)}")
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Primeiro, divide o documento por títulos.
        md_header_splits = markdown_splitter.split_text(content)
        
        # Depois, divide os pedaços grandes em pedaços menores.
        final_splits = chunk_splitter.split_documents(md_header_splits)
        
        # Adiciona a fonte (nome do ficheiro) a cada pedaço de texto para referência futura.
        for doc in final_splits:
            doc.metadata['source'] = os.path.basename(md_path)
            
        all_split_docs.extend(final_splits)

    if not all_split_docs:
        print("\nAVISO: Nenhum documento processado. A base de dados ficará vazia.")
        return

    # --- ETAPA 3: Gerar Embeddings e Salvar ---
    print(f"\nSucesso! {len(all_split_docs)} pedaços de texto gerados. A criar a base de vetores Chroma...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    if os.path.exists(PERSIST_DIRECTORY):
        print(f"A remover a base de dados antiga em '{PERSIST_DIRECTORY}'...")
        shutil.rmtree(PERSIST_DIRECTORY)

    vector_store = Chroma.from_documents(
        documents=all_split_docs, 
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print(f"\n--- SUCESSO! Nova base de vetores inteligente criada e salva em '{PERSIST_DIRECTORY}'! ---")

if __name__ == "__main__":
    build_and_save_vector_store()