# inspect_chunks.py

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv() # Garante que as variáveis de ambiente sejam carregadas

# --- Configurações ---
PERSIST_DIRECTORY = './backend-api/chroma_db' # Caminho para a base de dados vetorial

def inspect_vector_store():
    """
    Carrega a base de dados vetorial e busca por chunks relevantes
    para perguntas específicas, exibindo o conteúdo e os metadados.
    """
    print(f"--- INICIANDO INSPEÇÃO DA BASE DE VETORES EM '{PERSIST_DIRECTORY}' ---")

    # Verifica se o diretório da base de dados existe
    if not os.path.exists(PERSIST_DIRECTORY):
        print(f"ERRO: Diretório ChromaDB não encontrado em '{PERSIST_DIRECTORY}'. Certifique-se de que o script 'vector_store.py' foi executado com sucesso.")
        return

    try:
        # Inicializa o modelo de embeddings do Google
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Carrega a base de dados vetorial do diretório especificado
        vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
        print("Base de dados vetorial carregada com sucesso.")

        # --- Testes com Perguntas Específicas ---
        queries_to_test = [
            "testes pirolenhoso bambu tratamento preservativo", # Pergunta sobre dados de teste
            "espécies exóticas invasoras bambu Phyllostachys", # Pergunta sobre espécies invasoras
            "Arundo donax em áreas de preservação", # Pergunta sobre Arundo donax
        ]

        for query in queries_to_test:
            print(f"\n--- BUSCANDO POR CHUNKS RELACIONADOS A: '{query}' ---")
            
            # Busca os documentos mais relevantes usando a query
            # Usamos k=5 para ver os 5 chunks mais relevantes
            results = vector_store.similarity_search(query=query, k=5)

            if not results:
                print("Nenhum chunk encontrado para este termo de busca.")
                continue # Passa para a próxima query

            print(f"--- {len(results)} CHUNKS ENCONTRADOS PARA '{query}' ---")
            for i, doc in enumerate(results):
                print(f"\n--- Chunk {i+1} ---")
                print(f"Conteúdo:\n{doc.page_content}")
                print(f"\nMetadados:\n{doc.metadata}")
                print("-" * 30)
            print("\n" + "="*50 + "\n") # Separador entre queries

    except Exception as e:
        print(f"ERRO DURANTE A INSPEÇÃO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    inspect_vector_store()