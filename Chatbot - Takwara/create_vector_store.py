# vector_store.py

# -*- coding: utf-8 -*-
"""
VERSÃO ATUALIZADA: Garante o carregamento correto de PDFs,
adiciona metadados precisos de nome de arquivo e remove metadados
de "source" para evitar vazamento de fontes.
"""
import os
import shutil
import io
import tempfile
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from google.cloud import storage
from urllib.parse import quote
from pathlib import Path

# --- Configurações ---
load_dotenv()

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "takwara-bank")
DOCS_ROOT_FOLDER = './docs'
PERSIST_DIRECTORY = './backend-api/chroma_db' 
BASE_URL_SITE = "https://resck.github.io/Takwara-Tech/"
GENERIC_GCS_URL = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/"

MARKDOWN_HEADERS_TO_SPLIT_ON = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]

# --- Parâmetros para dividir documentos em pedaços (chunks) ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# --- Definição GLOBAL dos Splitters ---
# Define os splitters aqui para que sejam acessíveis em todo o arquivo
recursive_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=MARKDOWN_HEADERS_TO_SPLIT_ON)

# --- Funções Auxiliares ---

def get_url_from_file_path(file_path):
    """
    Gera uma URL amigável para arquivos Markdown a partir de seu caminho no sistema de arquivos.
    Exemplo: ./docs/A1. A Tecnologia Takwara/A1. Tecnologia Takwara/index.md
    -> https://resck.github.io/Takwara-Tech/A1.%20A%20Tecnologia%20Takwara/A1.%20Tecnologia%20Takwara/
    """
    try:
        p = Path(file_path)
        # Relativiza o caminho a partir da pasta raiz dos documentos
        relative_p = p.relative_to(DOCS_ROOT_FOLDER)
        # Remove a extensão do arquivo para criar a estrutura de URL
        path_without_ext = relative_p.with_suffix('')
        # Codifica cada parte do caminho para garantir que caracteres especiais sejam tratados corretamente
        url_parts = [quote(part) for part in path_without_ext.parts]
        url_path = "/".join(url_parts)
        # Monta a URL final usando a base do site
        final_url = f"{BASE_URL_SITE}{url_path}/"
        return final_url
    except Exception as e:
        print(f"Aviso: Erro ao gerar URL para '{file_path}': {e}. Usando URL base.")
        return BASE_URL_SITE

def load_docs_from_gcs(bucket_name):
    """
    Carrega todos os arquivos PDF de um bucket GCS especificado,
    processa-os em chunks e adiciona metadados relevantes (nome do arquivo).
    """
    print(f"\n--- A carregar documentos PDF do bucket '{bucket_name}' no GCS ---")
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        # Lista todos os objetos (arquivos) no bucket
        blobs = list(bucket.list_blobs())
        pdf_docs_loaded = [] # Lista para armazenar os documentos carregados (antes de dividir em chunks)
        pdf_count = len([b for b in blobs if b.name.lower().endswith('.pdf')]) # Conta quantos PDFs existem
        
        if pdf_count == 0:
            print("Aviso: Nenhum arquivo PDF encontrado no bucket.")
            return [] # Retorna lista vazia se nenhum PDF for encontrado
            
        # Itera sobre cada blob (arquivo) no bucket
        for blob in blobs: 
            # Processa apenas arquivos com extensão .pdf
            if blob.name.lower().endswith('.pdf'):
                print(f"  -> A processar: {blob.name}")
                temp_file_path = None # Inicializa caminho do arquivo temporário
                try:
                    # Cria um arquivo temporário para baixar o PDF
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                        blob.download_to_filename(temp_file.name)
                        temp_file_path = temp_file.name # Armazena o caminho do arquivo temporário
                    
                    # Carrega o documento PDF usando PyMuPDFLoader (mais robusto)
                    documents = PyMuPDFLoader(file_path=temp_file_path).load() 
                    
                    # Extrai o nome base do arquivo PDF original do blob
                    original_pdf_filename = os.path.basename(blob.name) if blob.name else 'unknown.pdf' 

                    # Adiciona metadados a cada documento (página ou seção) carregado do PDF
                    for doc in documents: 
                        doc.metadata['filename'] = original_pdf_filename # Armazena o nome do arquivo PDF
                        doc.metadata['source'] = original_pdf_filename # Usa 'source' para compatibilidade futura e para ser removido depois
                    
                    pdf_docs_loaded.extend(documents) # Adiciona os documentos carregados à lista geral

                finally:
                    # Garante que o arquivo temporário seja removido após o uso
                    if temp_file_path: 
                        os.remove(temp_file_path)
        
        # Agora, processamos os chunks a partir dos 'pdf_docs_loaded'
        processed_pdf_chunks = []
        for doc in pdf_docs_loaded: # Itera sobre os documentos carregados
            # Divide cada documento em chunks usando o splitter global
            pdf_chunks = recursive_splitter.split_documents([doc]) 
            for chunk in pdf_chunks: # Para cada chunk gerado
                # Garante que cada chunk de PDF tenha os metadados corretos
                # Pega o filename do metadado do documento original
                chunk.metadata['filename'] = doc.metadata.get('filename', 'unknown.pdf')
                # Adiciona também em 'source' para consistência com a limpeza posterior
                chunk.metadata['source'] = doc.metadata.get('source', 'unknown.pdf')
            processed_pdf_chunks.extend(pdf_chunks) # Adiciona os chunks processados à lista

        print(f"Sucesso! Carregados {len(pdf_docs_loaded)} documentos PDF e gerados {len(processed_pdf_chunks)} chunks.")
        return processed_pdf_chunks # Retorna os chunks de PDF processados

    except Exception as e:
        print(f"ERRO CRÍTICO ao acessar o bucket '{bucket_name}': {e}")
        import traceback
        traceback.print_exc() # Imprime o traceback completo para depuração
        return [] # Retorna lista vazia em caso de erro

# --- Função Principal ---
def build_and_save_vector_store():
    """
    Orquestra o processo de construção da base de dados vetorial:
    1. Carrega documentos .md locais.
    2. Carrega documentos .pdf do Google Cloud Storage.
    3. Divide todos os documentos em chunks.
    4. Adiciona metadados relevantes a cada chunk.
    5. Limpa metadados desnecessários (como 'source').
    6. Gera embeddings e salva a base vetorial no ChromaDB.
    """
    print("--- INICIANDO CRIAÇÃO DA BASE DE VETORES ---")

    # ETAPA 1: CARREGAR DOCUMENTOS
    print("\n[ETAPA 1/5] Carregando documentos Markdown (.md) locais...")
    # Configura o loader para buscar arquivos .md em todas as subpastas
    loader_md = DirectoryLoader(DOCS_ROOT_FOLDER, glob="**/*.md", loader_cls=TextLoader, recursive=True, show_progress=True)
    markdown_docs = loader_md.load() # Carrega os documentos Markdown
    print(f"Carregados {len(markdown_docs)} documentos Markdown.")
    
    # Carrega e processa os documentos PDF do GCS, retornando os chunks
    pdf_chunks_from_gcs = load_docs_from_gcs(GCS_BUCKET_NAME) 
    
    # Combina os documentos Markdown com os chunks de PDF processados
    all_docs = markdown_docs + pdf_chunks_from_gcs 
    
    print(f"Total de documentos (chunks Markdown + chunks PDF) combinados: {len(all_docs)}")

    # ETAPA 2: ADICIONAR METADADOS DE URL
    print("\n[ETAPA 2/5] Adicionando metadados de URL...")
    for doc in all_docs: # Itera sobre todos os documentos (ou chunks)
        # Metadados para Documentos Markdown
        source_path = doc.metadata.get('source', '')
        if source_path.lower().endswith('.md'):
            # Gera uma URL amigável para os arquivos Markdown
            doc.metadata['url'] = get_url_from_file_path(source_path)
        # Metadados para Documentos PDF (o 'filename' e 'source' já foram adicionados em load_docs_from_gcs)
        # Garantimos que um URL genérico do GCS esteja presente se não houver outro
        elif 'url' not in doc.metadata:
            doc.metadata['url'] = GENERIC_GCS_URL

    print("Metadados de URL adicionados.")

    # ETAPA 3: DIVIDIR DOCUMENTOS EM PEDAÇOS (CHUNKS)
    # Esta etapa já foi realizada DENTRO de load_docs_from_gcs para PDFs.
    # Agora, precisamos dividir os documentos Markdown em chunks usando o markdown_splitter.
    print("\n[ETAPA 3/5] Dividindo documentos Markdown em pedaços (chunks)...")
    chunks = [] # Lista para armazenar todos os chunks finais
    for doc in markdown_docs: # Itera sobre os documentos Markdown originais
        # Divide cada documento Markdown usando o splitter configurado para markdown
        doc_chunks = markdown_splitter.split_text(doc.page_content)
        for chunk in doc_chunks:
            # Copia os metadados do documento Markdown original para cada chunk gerado
            chunk.metadata = doc.metadata.copy() 
        chunks.extend(doc_chunks) # Adiciona os chunks de Markdown à lista final
    
    # Adiciona os chunks de PDF processados (que já vêm com metadados corretos) à lista final
    chunks.extend(pdf_chunks_from_gcs)
    
    print(f"Divisão concluída. Total de chunks gerados: {len(chunks)}")

    # ETAPA 4: LIMPEZA FINAL DE METADADOS
    print("\n[ETAPA 4/5] Limpando metadados 'source' de todos os chunks...")
    for chunk in chunks: # Itera sobre todos os chunks finais
        # Remove o metadado 'source' para evitar qualquer vazamento de informação da fonte original
        if 'source' in chunk.metadata:
            del chunk.metadata['source'] 
        # Os metadados 'filename' e 'url' (para PDFs) e 'url' (para MDs) são mantidos.

    print("Limpeza final de metadados concluída.")

    # ETAPA 5: GERAR EMBEDDINGS E SALVAR NO CHROMA DB
    print(f"\n[ETAPA 5/5] Gerando embeddings e salvando no ChromaDB em '{PERSIST_DIRECTORY}'...")
    try:
        # Inicializa o modelo de embeddings do Google
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Remove a base de dados antiga, se ela existir, para garantir uma instalação limpa
        if os.path.exists(PERSIST_DIRECTORY):
            print(f"Removendo base de dados antiga em '{PERSIST_DIRECTORY}'...")
            shutil.rmtree(PERSIST_DIRECTORY)
        
        # Cria a base de dados vetorial a partir dos chunks e seus metadados
        # O ChromaDB armazenará os vetores e os metadados associados
        Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=PERSIST_DIRECTORY)
        
        print(f"\n--- SUCESSO! Nova base de vetores criada em '{PERSIST_DIRECTORY}'! ---")
    except Exception as e:
        print(f"\nERRO FATAL na etapa final: {e}")
        import traceback
        traceback.print_exc() # Imprime o traceback completo para depuração
        exit(1) # Encerra o script com código de erro

# Bloco principal de execução
if __name__ == "__main__":
    build_and_save_vector_store() # Chama a função principal para iniciar o processo