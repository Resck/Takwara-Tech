# /Users/fabiotakwara/Documents/GitHub/Takwara-Tech/Chatbot - Takwara/create_vector_store.py
# --- VERSÃO FINAL OTIMIZADA, CORRIGIDA PARA DEPLOY E PROCESSAMENTO DE CONTEÚDO ---

import os
import shutil
from glob import glob
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document # Importar a classe Document explicitamente
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from git import Repo

# Carrega a chave de API do ficheiro .env
load_dotenv()

# --- Configurações Principais ---
# URL do seu repositório GitHub
REPO_URL = "https://github.com/Resck/Takwara-Tech.git" # <-- Confirme se esta URL está correta
# Caminho LOCAL para o repositório clonado (será uma pasta temporária)
REPO_PATH = "./temp_repo"
# ONDE a base de dados de vetores será salva.
# DEVE estar dentro da pasta backend-api para ser incluída no deploy da Cloud Function.
PERSIST_DIRECTORY = "./backend-api/chroma_db" # <-- Caminho corrigido para deploy


def update_repository(repo_path, repo_url):
    """Clona ou atualiza o repositório Git."""
    print(f"\nA garantir que o repositório '{repo_url}' está atualizado...")
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            origin = repo.remotes.origin
            origin.pull()
            print("Repositório atualizado.")
        except Exception as e:
            print(f"Erro ao atualizar o repositório em '{repo_path}': {e}. A tentar recriar o repositório.")
            try:
                shutil.rmtree(repo_path)
                Repo.clone_from(repo_url, repo_path)
                print("Repositório removido e clonado novamente.")
            except Exception as clone_e:
                 print(f"ERRO CRÍTICO: Falha ao recriar o repositório em '{repo_path}': {clone_e}")
                 raise clone_e

    else:
        try:
            Repo.clone_from(repo_url, repo_path)
            print(f"Repositório clonado em '{repo_path}'.")
        except Exception as e:
             print(f"ERRO CRÍTICO: Falha ao clonar o repositório em '{repo_path}': {e}")
             raise e


def load_and_split_documents(repo_local_path):
    """
    Encontra todos os ficheiros .md dentro da pasta 'docs' do repositório local,
    carrega-os e divide-os de forma inteligente (priorizando cabeçalhos, com fallback).
    """
    # O caminho para a pasta 'docs' dentro do repositório clonado
    # AJUSTE o nome da pasta 'Chatbot - Takwara' se a pasta for diferente
    docs_folder_path_in_repo = os.path.join(repo_local_path, 'Chatbot - Takwara', 'docs')
    
    print(f"\nA carregar e a dividir todos os documentos .md da pasta de documentos local do repositório: '{docs_folder_path_in_repo}'...")

    # Usa glob para encontrar todos os ficheiros .md de forma recursiva
    markdown_files = glob(os.path.join(docs_folder_path_in_repo, '**', '*.md'), recursive=True)

    if not markdown_files:
        print(f"AVISO: Nenhum ficheiro .md encontrado em '{docs_folder_path_in_repo}'.")
        return []

    all_final_chunks = []
    # Configuração do MarkdownHeaderTextSplitter para títulos H1 a H5 (aumentado)
    # Pode ajustar esta lista conforme os níveis de cabeçalho mais usados nos seus docs.
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"), # Adicionado
        ("#####", "Header 5")  # Adicionado
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)

    # Configuração do RecursiveCharacterTextSplitter para pedaços menores
    chunk_size = 512 # Tamanho ideal dos pedaços (ajuste se necessário)
    chunk_overlap = 50 # Sobreposição entre pedaços (para manter contexto)
    chunk_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    print(f"  -> Configuração de Chunking: Tamanho={chunk_size}, Sobreposição={chunk_overlap}")
    print(f"  -> Dividindo por cabeçalhos: {headers_to_split_on}")


    for md_path in markdown_files:
        relative_path_log = os.path.relpath(md_path, repo_local_path) # Caminho relativo à raiz do repositório clonado
        print(f"  -> Processando: {relative_path_log}")

        # --- Inicializar lista para Document objects ---
        documents_with_metadata = []

        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content or not content.strip():
                 print(f"    AVISO: Arquivo '{relative_path_log}' está vazio ou contém apenas espaços. Ignorando.")
                 continue # Pula para o próximo arquivo se estiver vazio

            # --- TENTATIVA 1: Dividir primeiro por cabeçalhos ---
            try:
                # markdown_splitter retorna uma lista de strings de texto
                md_header_text_splits = markdown_splitter.split_text(content)

                # Para cada pedaço de texto dividido por cabeçalho, criar um Document object com metadados
                for text_split in md_header_text_splits:
                     # VERIFICAR se text_split é realmente uma string e não está vazia
                     if isinstance(text_split, str) and text_split.strip():
                          doc = Document(page_content=text_split, metadata={"source": os.path.basename(md_path)})
                          documents_with_metadata.append(doc)
                     # else: ignora pedaços que não são strings válidas/não vazias

                # Dividir os Document objects resultantes usando o RecursiveCharacterTextSplitter
                if documents_with_metadata: # Só tenta a próxima divisão se a primeira gerou documentos válidos
                     final_splits_from_headers = chunk_splitter.split_documents(documents_with_metadata)
                     if final_splits_from_headers:
                         print(f"    -> Gerados {len(final_splits_from_headers)} pedaços usando cabeçalhos.")
                         all_final_chunks.extend(final_splits_from_headers)
                     else:
                          print(f"    AVISO: MarkdownHeaderTextSplitter gerou Documentos, mas RecursiveCharacterTextSplitter não gerou pedaços de '{relative_path_log}'.")
                else:
                     print(f"    AVISO: MarkdownHeaderTextSplitter não gerou pedaços de texto válidos ou com metadados de '{relative_path_log}'.")
                     # Se a primeira tentativa falhou, passamos para a TENTATIVA 2 (fallback)

            except Exception as e_header_split:
                 print(f"    AVISO: Erro durante a divisão por cabeçalhos em '{relative_path_log}': {e_header_split}. A tentar fallback...")
                 documents_with_metadata = [] # Reseta a lista para não misturar se algo parcial foi adicionado


            # --- TENTATIVA 2 (Fallback): Usar apenas RecursiveCharacterTextSplitter no conteúdo completo ---
            # Isso acontece se a tentativa 1 não gerou NENHUM pedaço final válido.
            if not documents_with_metadata: # Verificar se documents_with_metadata ainda está vazio após a tentativa 1
                 try:
                     print(f"    -> A tentar fallback: usar apenas RecursiveCharacterTextSplitter no conteúdo completo de '{relative_path_log}'.")

                     # Crie um Document object com o conteúdo COMPLETO do arquivo
                     full_doc = Document(page_content=content, metadata={"source": os.path.basename(md_path)})

                     # Dividir usando apenas o RecursiveCharacterTextSplitter
                     final_splits_fallback = chunk_splitter.split_documents([full_doc])

                     if final_splits_fallback:
                         print(f"    -> Gerados {len(final_splits_fallback)} pedaços no fallback.")
                         all_final_chunks.extend(final_splits_fallback)
                     else:
                         print(f"    AVISO: O RecursiveCharacterTextSplitter TAMBÉM não gerou pedaços para o conteúdo completo de '{relative_path_log}'.")

                 except Exception as e_fallback_split:
                      print(f"    AVISO: Erro durante o fallback de split em '{relative_path_log}': {e_fallback_split}.")


        except Exception as e_read:
            # Este bloco try captura erros de leitura do arquivo
            print(f"    ERRO inesperado ao ler ou processar o ficheiro '{relative_path_log}': {e_read}")
            # Continuar processando outros arquivos mesmo se um falhar


    print(f"\nProcessamento de documentos concluído. Gerados {len(all_final_chunks)} pedaços de texto no total.")
    return all_final_chunks


def build_and_save_vector_store():
    """
    Orquestra o processo completo de construção e salvamento da base de dados de vetores.
    """
    print("--- INICIANDO A CRIAÇÃO/ATUALIZAÇÃO DA BASE DE VETORES DA AVT ---")

    # ETAPA 1: Clonar ou atualizar o repositório local
    try:
        update_repository(REPO_PATH, REPO_URL)
    except Exception as e:
        print(f"\nSCRIPT ABORTADO: Não foi possível clonar ou atualizar o repositório. {e}")
        return # Aborta se o repositório não puder ser preparado


    # ETAPA 2: Carregar e dividir os documentos da sua pasta 'docs' local
    # Passa o caminho LOCAL do repositório clonado para a função de carregamento
    split_docs = load_and_split_documents(REPO_PATH)

    if not split_docs:
        print("\nNenhum documento .md processado gerou pedaços válidos. A encerrar o script. A base de dados não será criada/atualizada.")
        # Limpa a pasta temporária se nada foi processado
        if os.path.exists(REPO_PATH):
            try:
                shutil.rmtree(REPO_PATH)
                print("Pasta temporária do repositório removida.")
            except Exception as e:
                print(f"AVISO: Não foi possível remover a pasta temporária '{REPO_PATH}': {e}. Remova manualmente se necessário.")
        return

    # ETAPA 3: Gerar os embeddings e criar/atualizar a base de dados Chroma
    print(f"\nPronto para gerar embeddings para {len(split_docs)} pedaços de texto...")
    print("A inicializar o modelo de embeddings do Google...")

    try:
        # Certificar que a chave GOOGLE_API_KEY está disponível no ambiente
        if not os.getenv("GOOGLE_API_KEY"):
             print("ERRO: Variável de ambiente GOOGLE_API_KEY não encontrada. Verifique seu arquivo .env na raiz do diretório de execução.")
             raise ValueError("GOOGLE_API_KEY não configurada.")

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        print("Modelo de embeddings carregado com sucesso.")
    except Exception as e:
        print(f"\nERRO CRÍTICO: Falha ao inicializar o modelo de embeddings. Verifique a sua chave GOOGLE_API_KEY e as permissões na Google Cloud.")
        print(f"Detalhe do erro: {e}")
        # Limpa a pasta temporária em caso de erro crítico aqui também
        if os.path.exists(REPO_PATH):
            try:
                shutil.rmtree(REPO_PATH)
            except Exception as e:
                 print(f"AVISO: Não foi possível remover a pasta temporária '{REPO_PATH}' após erro de embedding: {e}.")
        return

    # Remove a base de dados antiga para garantir uma reconstrução limpa
    # Garante que a pasta backend-api existe antes de tentar remover a subpasta chroma_db
    # Assume que create_vector_store.py é executado na raiz do repo ou em Chatbot - Takwara, e backend-api está nessa pasta ou uma subpasta.
    # Vamos usar o caminho absoluto para garantir a remoção correta.
    # O PERSIST_DIRECTORY já é "./backend-api/chroma_db" ou similar

    if os.path.exists(PERSIST_DIRECTORY):
        print(f"A remover a base de dados antiga em '{PERSIST_DIRECTORY}'...")
        try:
            shutil.rmtree(PERSIST_DIRECTORY)
            print("Base de dados antiga removida.")
        except Exception as e:
             print(f"AVISO: Não foi possível remover a base de dados antiga em '{PERSIST_DIRECTORY}': {e}. Verifique permissões ou remova manualmente.")


    print(f"A criar a nova base de vetores Chroma em '{PERSIST_DIRECTORY}'. Isto pode demorar alguns minutos...")

    try:
        # Garante que o diretório de persistência existe antes de criar a base
        os.makedirs(os.path.dirname(PERSIST_DIRECTORY), exist_ok=True) # Cria a pasta pai (backend-api) se não existir

        vector_store = Chroma.from_documents(
            documents=split_docs,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )
        print(f"\n--- SUCESSO! Nova base de vetores criada e salva em '{PERSIST_DIRECTORY}'! ---")

    except Exception as e:
         print(f"\nERRO CRÍTICO: Falha ao criar e salvar a base de dados Chroma em '{PERSIST_DIRECTORY}'. Verifique as permissões de escrita na pasta, espaço em disco e a sua conexão.")
         print(f"Detalhe do erro: {e}")

    finally:
        # ETAPA FINAL: Limpar a pasta temporária do repositório clonado (SEMPRE)
        print(f"A limpar a pasta temporária do repositório: '{REPO_PATH}'...")
        if os.path.exists(REPO_PATH):
            try:
                shutil.rmtree(REPO_PATH)
                print("Pasta temporária removida.")
            except Exception as e:
                print(f"AVISO: Não foi possível remover a pasta temporária '{REPO_PATH}': {e}. Remova manualmente se necessário.")


if __name__ == "__main__":
    # Quando o script é executado diretamente, roda a função principal
    build_and_save_vector_store()