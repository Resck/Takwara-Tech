# /Users/fabiotakwara/Documents/GitHub/Takwara-Tech/Chatbot - Takwara/backend-api/main.py
# VERSÃO FINAL, CORRIGIDA E COMPLETA PARA GOOGLE CLOUD FUNCTION (ERRO DE SINTAXE)

import os
import functions_framework
from flask import Flask, request, jsonify, make_response
# dotenv pode ser útil para rodar localmente, mas em Cloud Functions geralmente as variáveis são setadas diretamente no ambiente
# from dotenv import load_dotenv 
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.documents import Document # Importar Document para type hinting ou manipulação se necessário

# Carregar variáveis de ambiente se estiver rodando localmente (ex: para testar a API localmente)
# Em Cloud Functions, GOOGLE_API_KEY e outras vars devem ser configuradas no ambiente da função.
# load_dotenv() 

# O Flask app é necessário para functions_framework.http
app = Flask(__name__)

# --- Variáveis Globais para a Instância da Cloud Function ---
# Estes serão carregados uma vez por instância e reutilizados em múltiplos pedidos.
qa_chain = None
vector_store = None
embeddings = None
llm = None
# PROMPT já é um objeto global definido abaixo

# Diretório onde a base de dados ChromaDB PERSISTE (deve estar dentro da pasta do deploy)
# Em Cloud Functions, esta pasta estará na raiz do ambiente de execução da função.
PERSIST_DIRECTORY = "./chroma_db" # <-- Caminho relativo dentro do ambiente da função

# --- O Cérebro da AVT: Template de Prompt (Definido uma vez globalmente) ---
# Este é o prompt que define a persona e as instruções para o LLM
prompt_template = """
You are a helpful and cordial virtual assistant for Takwara-Tech, an expert in sustainable construction with bamboo and socio-environmental responsibility.

Your mission is to answer questions based ONLY on the information provided in the following context documents about the "Tecnologia Takwara" project.

Analyze the user's question to determine its language. YOU MUST RESPOND IN THE SAME LANGUAGE AS THE QUESTION.
If the user's question has spelling or grammatical errors, interpret it to the best of your ability and answer the most likely intended question.
If the answer to a user's question is not found within the provided context documents, politely state this limitation in the user's language.

When answering user queries, strive for the following qualities:

*   **Didactic:** Explain concepts clearly and logically, breaking down complex ideas found in the text (like the methodology components, the workflow, or the impact potential) into easily digestible parts. Use the structure and examples provided in the document to guide your explanations.
*   **Engaging:** Use language that captures interest and reflects the passion and vision expressed in the text (e.g., the urgency of the challenge, the potential for transformation, the collaborative spirit). You can use metaphors or analogies suggested by the text (like "aço vegetal" or "solda verde"). Frame the information in a way that connects with the user's potential interest areas (architecture, engineering, sustainability, community work).
*   **Stimulating:** Encourage the user's curiosity about the technology and its potential. Highlight the innovation and the forward-looking aspects.
*   **Creative & Interpretative:** Go beyond simply repeating phrases. Interpret the meaning and significance of the information *within the context of the document*. For example, when explaining a methodology component, explain *why* it's innovative or *what problem* it solves, according to the text. Connect different parts of the document where relevant (e.g., how the ecological treatment supports the use in geodésicas, or how ecomaterials address waste and contribute to ODS). Explain the *implications* of the information presented.

**Specific Instructions & Interaction Style:**

*   Your responses must be formatted using **Markdown** to improve readability and understanding.
*   Never provide simplistic answers when there is ample content available in the context documents. Always refer to the source documents to extract and present the maximum relevant information for each query, summarizing and synthesizing information from various relevant sections.
*   As an assistant, you will encourage the user to ask more complex and specific questions. Occasionally conclude your response with a thought-provoking statement, a question for further exploration, or by suggesting related areas based on the information discussed (e.g., "This section talks about ecomaterials. Would you like to know more about the specific types of waste used, or perhaps how they contribute to the ODS mentioned?").
*   At the end of your answer, if possible, **cite the source document(s)** (e.g., the title or file name like "index.md", "Artigos/documentação técnica Takwara/forno ecologico.md") from where you extracted the information. If information comes from multiple documents, list them.
*   When referencing the project's origin or creator, mention Fabio "Takwara" Resck as the idealizer, acknowledging the collective "Nós" as explained in the text (the spirit of collaboration and all contributors, past and present).
*   Mention that the material is open knowledge licensed under Creative Commons Attribution 4.0 International (CC BY 4.0) when discussing sharing, use, or contribution.
*   Maintain a positive, cordial, encouraging, and informative tone consistent with the document's spirit.

Your ultimate goal is to serve as a comprehensive, engaging, and inspiring guide to the "Tecnologia Takwara" project, empowering users by clearly and thoroughly explaining its principles, methodologies, and potential, always rooted in the provided documentation.

Context (Documents):
{context}

Question:
{question}

Helpful and cordial answer in the user's language:
"""
# Cria o objeto PromptTemplate
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


def load_qa_chain():
    """
    Carrega o modelo de embeddings, a base de vetores ChromaDB, o modelo LLM
    e configura a cadeia RAG com um retriever (MultiQuery com filtro contextual).
    Esta função é chamada no primeiro pedido para uma nova instância da função.
    """
    global qa_chain, vector_store, embeddings, llm # Acessa as variáveis globais

    print("--- Iniciando o carregamento global da base de vetores e do modelo LLM ---")

    try:
        # A Memória da AVT: Carregar o modelo de embeddings
        print("A carregar o modelo de embeddings do Google...")
        # Certificar que a chave GOOGLE_API_KEY está disponível no ambiente
        if not os.getenv("GOOGLE_API_KEY"):
             print("ERRO: Variável de ambiente GOOGLE_API_KEY não encontrada durante o carregamento. Configure no ambiente da Cloud Function.")
             # Retorna sem carregar nada se a chave não estiver setada
             qa_chain = None
             return

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        print("Modelo de embeddings carregado.")

        # A Memória da AVT: Carregar a base de dados de vetores ChromaDB
        # O caminho PERSIST_DIRECTORY deve ser onde a pasta 'chroma_db' foi colocada durante o deploy.
        print(f"A carregar a base de vetores Chroma de '{PERSIST_DIRECTORY}'...")
        # Verifica se o diretório existe E contém arquivos (verificação mais robusta)
        if not os.path.exists(PERSIST_DIRECTORY) or not os.listdir(PERSIST_DIRECTORY):
            print(f"ERRO CRÍTICO: Diretório de persistência ChromaDB não encontrado ou está vazio em {PERSIST_DIRECTORY}. A base de dados não foi criada ou incluída no deploy?")
            qa_chain = None # Falha crítica
            return

        vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
        print("Base de vetores Chroma carregada.")

        # O Raciocínio da AVT: Carregar o modelo de linguagem (LLM)
        print("A carregar o modelo LLM Gemini-1.5-Pro...")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3) # temperature=0.3 sugere respostas mais consistentes
        print("Modelo LLM carregado.")


        # --- Configurar o Retriever Base para MultiQuery (sem filtro inicial) ---
        # Este retriever será usado pelo MultiQuery para buscas gerais.
        base_retriever_general = vector_store.as_retriever(
             search_type="mmr",  # Usa Maximal Marginal Relevance para diversificar
             search_kwargs={"k": 6} # Busca 6 documentos por padrão na busca geral
        )
        print("Retriever base para MultiQuery configurado.")


        # --- Configurar o MultiQuery Retriever ---
        # Este é o retriever principal que a cadeia RAG usará.
        # Ele usa o LLM para gerar consultas alternativas e o base_retriever_general para buscá-las.
        print("A configurar o MultiQuery Retriever...")
        retriever_multi_query = MultiQueryRetriever.from_llm(
             retriever=base_retriever_general, # Usa o retriever base que já pode ter MMR/k configurado
             llm=llm,
             # prompt_template="...", # Opcional: prompt customizado para o MultiQuery LLM
        )
        print("MultiQuery Retriever configurado.")


        # --- Configurar a Cadeia RAG (Retrieval Augmented Generation) ---
        print("A montar a cadeia RetrievalQA...")
        # A cadeia usa o LLM e o retriever_multi_query por padrão.
        # A lógica de busca contextual (filtrar por fonte) será aplicada *antes* de chamar a cadeia.
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff", # 'stuff' para usar todos os documentos encontrados no prompt
            retriever=retriever_multi_query, # Usamos o MultiQueryRetriever aqui por enquanto
            chain_type_kwargs={"prompt": PROMPT}, # Passa o nosso PromptTemplate
            return_source_documents=True # Queremos que a cadeia retorne os documentos fonte para citar
        )
        print(">>> Cadeia RetrievalQA com MultiQuery configurada! <<<")

    except Exception as e:
        print(f"ERRO CRÍTICO GERAL DURANTE O CARREGAMENTO: {e}")
        import traceback
        traceback.print_exc() # Imprime o traceback completo nos logs
        qa_chain = None
        vector_store = None
        embeddings = None
        llm = None


@functions_framework.http
def chatbot_api(request):
    """
    Manipulador de requisições HTTP para a Google Cloud Function.
    Recebe a pergunta do usuário e o contexto (URL da página),
    realiza a busca contextual e retorna a resposta da AVT.
    """
    # --- Configuração CORS (Permite requisições de qualquer origem) ---
    headers = {'Access-Control-Allow-Origin': '*'}

    # --- Manipulação de requisições OPTIONS (para CORS preflight) ---
    if request.method == 'OPTIONS':
        print("Recebida requisição OPTIONS. Respondendo para CORS.")
        response = make_response('', 204) # No Content
        # Permite os métodos e cabeçalhos que o frontend pode usar
        headers.update({
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        })
        response.headers.extend(headers)
        return response # Retorna a resposta para OPTIONS e encerra a execução

    # --- Se o método não for OPTIONS, continua processando ---

    # --- Carregamento "Lazy": Carrega a cadeia se ainda não foi carregada nesta instância ---
    # Isso acontece no primeiro pedido para uma nova instância ou após um cold start.
    global qa_chain, vector_store # Acessa variáveis globais
    
    if qa_chain is None:
        print("Cadeia de IA não carregada nesta instância. Tentando carregar agora...")
        load_qa_chain()
        # Após tentar carregar, verifica novamente se foi bem sucedido
        if qa_chain is None:
             print("Falha no carregamento da cadeia após a tentativa. Retornando erro 500.")
             return (jsonify({"error": "O sistema de IA falhou ao carregar. Verifique os logs da função."}), 500, headers)


    # --- Processar requisições POST com a pergunta do usuário ---
    if request.method == 'POST': # Verifica explicitamente se é um método POST
        request_json = request.get_json(silent=True)

        # Verificar se o request JSON é válido e contém a pergunta
        if not request_json or 'query' not in request_json:
             print("Recebido pedido inválido: JSON ausente ou sem 'query'.")
             return (jsonify({"error": "Pedido inválido. Por favor, forneça uma pergunta no corpo JSON."}), 400, headers)

        query = request_json['query']
        context_url = request_json.get('context') # Pega o contexto (URL) se existir

        print(f"Recebida pergunta: '{query}' (Contexto: {context_url})")

        # --- Respostas Pré-definidas para saudações ---
        if query.lower().strip() in ["olá", "oi", "ola", "hello", "hi"]:
            # Podemos usar o LLM para gerar a saudação no idioma correto
            try:
                 # Tenta usar o LLM carregado para gerar a saudação contextualizada
                 if llm is not None: # Garante que o LLM foi carregado
                      # Prompt simples para gerar saudação no idioma detectado ou padrão
                      greeting_prompt_text = f"Gere uma saudação cordial e breve no idioma da pergunta '{query}' ou no idioma padrão português, apresente-se como a assistente virtual Takwara, expert em construção sustentável com bambu, e pergunte como pode ajudar."
                      llm_greeting_response = llm.invoke(greeting_prompt_text)
                      greeting_text = llm_greeting_response.content
                      print(f"Gerada saudação com LLM: {greeting_text}")
                      return (jsonify({"answer": greeting_text}), 200, headers)
                 else:
                      print("LLM não carregado. Retornando saudação padrão.")
                      return (jsonify({"answer": "Olá, eu sou a assistente virtual Takwara. Em que posso ajudar?"}), 200, headers)

            except Exception as e:
                 print(f"AVISO: Erro ao tentar gerar saudação com LLM: {e}. Retornando saudação padrão.")
                 return (jsonify({"answer": "Olá, eu sou a assistente virtual Takwara. Em que posso ajudar?"}), 200, headers) # Retorna saudação padrão em caso de falha

        # --- A Audição e o Raciocínio da AVT: Processar a pergunta com RAG ---
        try:
            # Acessa o vector_store global para busca filtrada, se ele foi carregado
            if vector_store is None:
                 print("ERRO: Vector store não carregado. Não é possível realizar busca.")
                 raise RuntimeError("Vector store not loaded.") # Lança um erro para ser capturado abaixo


            # Acessa o retriever original MultiQuery configurado globalmente
            retriever_para_uso = qa_chain.retriever # Este é o MultiQueryRetriever

            # --- Lógica de Busca Contextual (Priorizar página atual) ---
            # Verifica se há um contexto (URL) e se não é a raiz ou a página do chatbot
            # A lógica de mapeamento de URL para nome de arquivo fonte pode precisar de ajuste fino
            # dependendo da sua configuração específica do MkDocs e nomes de arquivos.
            source_file_name = None
            if context_url and context_url != "/" and context_url != "/chatbot/":
                 try:
                     # Remove barras iniciais/finais, substitui %20 por espaço, pega a última parte e adiciona .md
                     cleaned_url_part = context_url.strip('/').replace('%20', ' ')
                     # Tenta pegar a última parte que parece um nome de arquivo (ex: /caminho/para/arquivo -> arquivo)
                     source_file_name = os.path.basename(cleaned_url_part) + ".md"
                     print(f"Contexto identificado. Nome de arquivo fonte presumido: '{source_file_name}' (do URL '{context_url}')")

                     # Opcional: Verificação adicional se o nome parece válido (evita lixo do URL)
                     # if not source_file_name or len(source_file_name) > 50: # Exemplo: muito longo
                     #    source_file_name = None
                     #    print("Nome de arquivo presumido inválido. Ignorando busca contextual.")

                 except Exception as e:
                     print(f"AVISO: Erro ao tentar extrair nome de arquivo do contexto '{context_url}': {e}. A fazer busca geral.")
                     source_file_name = None # Reseta para forçar busca geral


            retrieved_docs = [] # Inicializa a lista de documentos recuperados

            # --- Executa a Busca ---
            if source_file_name and source_file_name != ".md": # Verifica se um nome de arquivo válido foi extraído (não apenas ".md")
                 try:
                     # Tenta buscar documentos APENAS deste ficheiro fonte na base de dados filtrando por metadados 'source'
                     # Cria um retriever TEMPORÁRIO SÓ COM O FILTRO
                     context_retriever_filtered = vector_store.as_retriever(
                          search_kwargs={'filter': {'source': source_file_name}, "k": 5} # Buscar até 5 docs específicos no contexto
                     )

                     print(f"A procurar documentos SOMENTE em '{source_file_name}' para a pergunta: '{query}'")
                     retrieved_docs = context_retriever_filtered.get_relevant_documents(query)

                     if context_docs: # Se encontrou documentos no contexto filtrado
                         print(f"Encontrados {len(context_docs)} documentos relevantes no contexto '{source_file_name}'.")
                         # Usa ESTES documentos para a cadeia RAG. Não precisa da busca geral neste caso.
                         # (Não fazemos a busca geral fallback se a busca contextual retornou algo)
                         pass # retrieved_docs já está populado com context_docs

                     else:
                         print(f"Nenhum documento relevante encontrado SOMENTE em '{source_file_name}'.")
                         # Se não encontrou NADA no contexto específico, FAZ a busca geral usando o MultiQuery
                         print("A fazer busca geral usando o MultiQueryRetriever.")
                         retrieved_docs = retriever_para_uso.get_relevant_documents(query) # Usa o retriever_multi_query configurado globalmente


                 except Exception as e:
                      print(f"AVISO: Erro durante a busca filtrada por contexto ('{source_file_name}') em '{context_url}': {e}. A fazer busca geral.")
                      # Em caso de erro na busca filtrada, faz a busca geral como fallback
                      retrieved_docs = retriever_para_uso.get_relevant_documents(query) # Usa o retriever_multi_query

            else: # Se não há contexto de página válido ou o nome do arquivo extraído é inválido
                 print("Sem contexto de página válido. A fazer busca general usando o MultiQueryRetriever.")
                 # Simplesmente faz a busca geral usando o MultiQuery
                 retrieved_docs = retriever_para_uso.get_relevant_documents(query)


            # --- Executar a cadeia RAG com os documentos recuperados ---
            if not retrieved_docs:
                print("Nenhum documento relevante foi recuperado para a busca final (lista retrieved_docs está vazia).")
                # Se NENHUM documento foi recuperado (mesmo na busca geral fallback), o modelo não terá contexto.
                # Podemos retornar uma mensagem padrão aqui.
                # Ou deixar o LLM responder com base no prompt (que dirá que não encontrou).
                # Vamos deixar o LLM tentar responder com base no prompt, que é mais gracioso.
                # result = {"output_text": "Desculpe, não encontrei informações relevantes nos meus documentos sobre isso."} # Exemplo de resposta padrão

                # Passar uma lista vazia de documentos para a cadeia é válido e o prompt cuidará disso.
                pass # Continua para o invoke mesmo com retrieved_docs vazio


            print(f"Documentos recuperados para a cadeia ({len(retrieved_docs)}): {[doc.metadata.get('source', 'desconhecida') for doc in retrieved_docs]}")

            # O chain_type="stuff" espera input_documents e a question no invoke
            # Usamos o qa_chain.combine_documents_chain diretamente
            result = qa_chain.combine_documents_chain.invoke({
                 "input_documents": retrieved_docs, # Passa a lista de Document objects recuperados
                 "question": query
            })

            # Acessar a resposta e os documentos fonte do resultado
            answer = result.get('output_text', 'Não foi possível extrair uma resposta útil dos documentos.')

            # Extrair fontes dos metadados dos documentos recuperados
            sources = [doc.metadata.get('source', 'desconhecida') for doc in retrieved_docs]
            unique_sources = list(set(sources)) # Remove duplicatas

            # Adicionar fontes à resposta se existirem
            if unique_sources:
                # Formata a citação das fontes no final da resposta
                answer += f"\n\nFonte(s): {', '.join(unique_sources)}"

            print(f"Resposta gerada. Fontes: {unique_sources}")

            # Retornar a resposta e as fontes no formato esperado pelo frontend
            return (jsonify({"answer": answer, "sources": unique_sources}), 200, headers)

        except Exception as e:
            # Captura erros durante o processo RAG
            print(f"ERRO INESPERADO DURANTE O PROCESSAMENTO DA PERGUNTA: {e}")
            import traceback
            traceback.print_exc() # Imprime o traceback completo nos logs da função
            # Retorna uma mensagem de erro genérica para o usuário no frontend
            return (jsonify({"error": f"Ocorreu um erro interno ao processar sua pergunta. Por favor, tente novamente. (Detalhes técnicos nos logs da função)"}), 500, headers)

    # --- Se o método HTTP não for OPTIONS ou POST, retorna 405 ---
        else: # ALINHADO com o primeiro 'if request.method == ...'
            print(f"Recebido método HTTP não permitido: {request.method}")
            return (jsonify({"error": f"Método '{request.method}' não permitido."}), 405, headers)


    # --- Ponto de entrada para execução local (para testar a API no seu computador) ---
    # Se rodar este arquivo diretamente (python main.py), ele iniciará um servidor Flask local.
    # Certifique-se de ter GOOGLE_API_KEY no seu .env (na raiz do diretório de execução) e a pasta ./chroma_db com a base de dados.
    # Para testar localmente, navegue até a pasta Chatbot - Takwara/backend-api no terminal e execute 'python main.py'
    if __name__ == "__main__":
        print("\n--- RODANDO API LOCALMENTE PARA TESTES ---")
        # Carrega a cadeia globalmente na inicialização do servidor local
        load_qa_chain()
        if qa_chain is not None:
            print("API local pronta para receber pedidos na porta 8080.")
            # Usa o servidor de desenvolvimento do Flask (não recomendado para produção)
            # debug=True pode ser útil para ver logs detalhados localmente
            # host='0.0.0.0' permite acesso de outras máquinas na rede local
            app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), debug=True)
        else:
            print("Não foi possível carregar a cadeia de IA. API local não iniciada.")
            print("Verifique os erros críticos durante o carregamento.")