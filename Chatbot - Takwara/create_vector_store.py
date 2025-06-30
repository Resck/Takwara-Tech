# -*- coding: utf-8 -*-
"""
VERSÃO FINAL: Foco em persistência LOCAL do ChromaDB.
Processa documentos Markdown (.md) da pasta local 'docs/',
gera chunks, embeddings e salva a base vetorial LOCALMENTE
no diretório './backend-api/chroma_db'.
Esta versão NÃO depende de Google Cloud Storage.
"""

import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pathlib import Path
from urllib.parse import quote # Usado para codificar caminhos em URLs (para metadados)
import traceback # Para logar erros detalhados

# --- Configurações ---
load_dotenv() # Carrega variáveis de ambiente (ex: GOOGLE_API_KEY)

# --- Configurações de Carregamento e Split ---
DOCS_ROOT_FOLDER = './docs' # Pasta onde estão os arquivos .md
PERSIST_DIRECTORY = './backend-api/chroma_db' # Diretório LOCAL para salvar a base de dados ChromaDB
BASE_URL_SITE = "https://resck.github.io/Takwara-Tech/" # Mantido para metadados de URL dos .md

# --- Parâmetros para dividir documentos em pedaços (chunks) ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# --- Definição GLOBAL dos Splitters ---
# Splitter para Markdown, que considera a estrutura de cabeçalhos
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")])
# Splitter recursivo padrão para outros tipos de texto ou caso o markdown_splitter falhe
recursive_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

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
        return BASE_URL_SITE # Retorna URL base em caso de falha

# --- Função Principal ---
def build_and_save_vector_store():
    """
    Orquestra o processo de construção da base de dados vetorial LOCAL:
    1. Carrega documentos Markdown (.md) locais.
    2. Divide os documentos em chunks.
    3. Adiciona metadados de URL a cada chunk.
    4. Limpa metadados desnecessários ('source').
    5. Gera embeddings e salva a base vetorial LOCALMENTE no ChromaDB.
    """
    print("--- INICIANDO CRIAÇÃO DA BASE DE VETORES LOCAL ---")

    # ETAPA 1: CARREGAR DOCUMENTOS MARKDOWN (.md)
    print(f"\n[ETAPA 1/4] Carregando documentos Markdown (.md) da pasta local: '{DOCS_ROOT_FOLDER}'...")
    if not os.path.isdir(DOCS_ROOT_FOLDER):
         print(f"\nErro: Diretório de documentos públicos não encontrado: '{DOCS_ROOT_FOLDER}'")
         exit(1)
    
    # Configura o loader para buscar APENAS arquivos .md na pasta especificada
    loader_md = DirectoryLoader(
        DOCS_ROOT_FOLDER,
        glob="**/*.md", # Busca todos os arquivos .md em todas as subpastas
        loader_cls=TextLoader,
        recursive=True,
        show_progress=True
        # load_data=True foi removido, pois causava TypeError em versões anteriores
    )
    markdown_docs = loader_md.load() # Carrega os documentos Markdown
    print(f"Carregados {len(markdown_docs)} documentos .md.")

    if not markdown_docs: # Verifica se algum documento .md foi carregado
        print("\nERRO FATAL: Nenhum documento .md foi carregado. Verifique a pasta './docs/'. Abortando.")
        exit(1)

    # ETAPA 2: ADICIONAR METADADOS DE URL aos documentos Markdown
    print("\n[ETAPA 2/4] Adicionando metadados de URL aos documentos Markdown...")
    for doc in markdown_docs:
        source_path = doc.metadata.get('source', '') # Pega o caminho do arquivo .md
        if source_path: # Se o caminho do arquivo for encontrado
            doc.metadata['url'] = get_url_from_file_path(source_path) # Gera e adiciona a URL
        else:
            doc.metadata['url'] = BASE_URL_SITE # Fallback para URL base se o caminho não for claro

    print("Metadados de URL adicionados aos documentos Markdown.")

    # ETAPA 3: DIVIDIR DOCUMENTOS MARKDOWN EM PEDAÇOS (CHUNKS)
    print("\n[ETAPA 3/4] Dividindo documentos Markdown em pedaços (chunks)...")
    chunks = [] # Lista para armazenar todos os chunks finais
    for doc in markdown_docs: # Itera sobre os documentos Markdown carregados
        try:
            # Usa o MarkdownHeaderTextSplitter para dividir o conteúdo dos .md com base nos cabeçalhos
            doc_chunks = markdown_splitter.split_text(doc.page_content)
            for chunk in doc_chunks:
                # Copia os metadados do documento original (incluindo a URL) para cada chunk gerado
                chunk.metadata = doc.metadata.copy() 
            chunks.extend(doc_chunks) # Adiciona os chunks de Markdown à lista final
        except Exception as e:
            print(f"Erro ao dividir o documento '{doc.metadata.get('source')}': {e}. Usando fallback de split.")
            # Fallback para o splitter recursivo se houver problema com o markdown splitter
            fallback_chunks = recursive_splitter.split_documents([doc])
            for chunk in fallback_chunks:
                chunk.metadata = doc.metadata.copy() # Mantém os metadados
            chunks.extend(fallback_chunks)
    
    print(f"Divisão concluída. Total de chunks gerados: {len(chunks)}")

    if not chunks: # Verifica se algum chunk foi gerado
        print("\nERRO FATAL: Nenhum chunk foi gerado após o processamento dos documentos. Abortando.")
        exit(1)

    # ETAPA 4: GERAR EMBEDDINGS E SALVAR NO CHROMA DB LOCAL
    print(f"\n[ETAPA 4/4] Gerando embeddings e salvando no ChromaDB local em '{PERSIST_DIRECTORY}'...")
    try:
        # Verifica se a chave de API do Google está definida (necessária para embeddings)
        if not os.getenv("GOOGLE_API_KEY"):
             print("\nErro: GOOGLE_API_KEY não encontrada. Certifique-se de que está definida no ambiente.")
             exit(1)
        # Inicializa o modelo de embeddings do Google
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        print("Modelo de embeddings carregado com sucesso.")
        
        # Remove a base de dados local antiga, se ela existir, para garantir uma instalação limpa
        if os.path.exists(PERSIST_DIRECTORY):
            print(f"Removendo base de dados local antiga em '{PERSIST_DIRECTORY}'...")
            shutil.rmtree(PERSIST_DIRECTORY)
        
        # Cria a base de dados vetorial ChromaDB localmente
        # ChromaDB gerencia a persistência no disco no diretório especificado
        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY # Salva localmente
        )
        
        print(f"\n--- SUCESSO! Nova base de vetores UNIFICADA criada LOCALMENTE em '{PERSIST_DIRECTORY}'! ---")
        
    except Exception as e:
        print(f"\nERRO FATAL na etapa final de criação do ChromaDB local: {e}")
        import traceback
        traceback.print_exc() # Imprime o traceback completo para depuração
        exit(1)

if __name__ == "__main__":
    build_and_save_vector_store()