Relatório Consolidado e Manual de Operação do Projeto Takwara Tech
Este documento detalha a arquitetura, o processo de desenvolvimento, o histórico de desafios e o fluxo de trabalho prático para gerir e atualizar o portal de documentação interativo e sua Assistente Virtual (AVT) integrada.

1. Arquitetura da Solução Final
O projeto é dividido em duas componentes principais: o Frontend, responsável pela apresentação do site e pela interface do utilizador, e o Backend, que abriga a inteligência da assistente virtual.

1.1. Backend: A Assistente Virtual (AVT)
A AVT é uma API "serverless" (sem servidor) publicada na Google Cloud que utiliza um sistema de Busca Aumentada por Geração (RAG) para fornecer respostas contextuais.

Plataforma: Google Cloud Function (Geração 2, Python 3.11, 512MB de memória) na região southamerica-east1.
Stack de IA:
Orquestração: Langchain
Modelo de Linguagem (LLM): Google Generative AI (Gemini 1.5 Flash)
Base de Dados Vetorial: ChromaDB
Ficheiros Essenciais (/backend-api):
create_vector_store.py: Script responsável por clonar o repositório, dividir os documentos (.md, .py, .txt) usando MarkdownHeaderTextSplitter e criar uma base de dados vetorial (chroma_db/).
main.py: O código da API. Recebe uma pergunta, usa um MultiQueryRetriever para fazer uma busca abrangente na base vetorial e, com a ajuda de um PromptTemplate customizado, gera uma resposta cordial e contextualizada.
requirements.txt: Lista minimalista de dependências Python essenciais para o funcionamento da API na nuvem.
.env: Ficheiro local para armazenar a chave GOOGLE_API_KEY durante o desenvolvimento.
1.2. Frontend: O Portal de Documentação
O site é gerado estaticamente com MkDocs, permitindo que seja hospedado gratuitamente e com eficiência no GitHub Pages.

Tecnologia: MkDocs com o tema Material for MkDocs.
Estrutura e Layout:
Layout de 3 Colunas: A aparência foi customizada via CSS (custom.css) para exibir uma estrutura de 3 colunas: navegação principal fixa à esquerda, conteúdo no centro e o índice do artigo à direita.
Navegação e Estrutura: O ficheiro mkdocs.yml define toda a estrutura de navegação, aparência e extensões do site.
Customização Avançada: Foram usados "overrides" (overrides/partials/footer.html) para modificar componentes do tema, como o rodapé.
2. Histórico de Desafios e Soluções (Debugging)
A estabilização do projeto envolveu a resolução de uma cascata de problemas interligados.

Problema: Falha no Deploy (Container Healthcheck Failed).

Solução: Criação de um requirements.txt exclusivo e minimalista para a API, removendo dependências incompatíveis do MkDocs.
Problema: API "congelava" e retornava erro de Timeout (300-504s).

Solução: Uma abordagem em múltiplas frentes:
A memória da função foi aumentada para 512MB.
Foram atribuídos os papéis de IAM "Usuário do Vertex AI" e "Cloud Build Builder".
A base de dados vetorial (chroma_db) foi reconstruída para corrigir corrupção de dados.
Problema: Base de conhecimento da AVT estava desatualizada.

Solução: Remoção da entrada chroma_db/ do ficheiro .gcloudignore para permitir que a base de dados fosse incluída no deploy.
3. Manual de Operação: Fluxo de Trabalho no VS Code
Este guia prático detalha o ciclo de trabalho completo para atualizar o portal e a AVT.

3.1. Os "Painéis de Controlo" do Projeto
Para gerir este projeto, é essencial entender três ficheiros de configuração:

mkdocs.yml (O "Arquiteto" do Site):
Localização: Na pasta raiz do projeto.
Função: Controla a estrutura de navegação, tema, metadados e extensões do site.
.gitignore (O "Porteiro" do Repositório):
Localização: Na pasta raiz do projeto.
Função: Lista ficheiros e pastas a serem ignorados pelo Git (ex: .venv/, temp_repo/, site/), mantendo o repositório limpo.
requirements.txt (A "Lista de Ingredientes"):
Localização: Existem versões específicas dentro de backend-api/ e calculadora-api/.
Função: Define os pacotes Python que cada API precisa para funcionar.
3.2. O Ciclo de Desenvolvimento Completo
Siga estes passos desde o início do trabalho até à publicação das alterações.

Passo 1: Preparar o Ambiente de Trabalho

Sempre que iniciar uma sessão de trabalho, abra um novo terminal no VS Code e execute:

Bash

# Navegue para a pasta principal do projeto (ajuste o caminho se necessário)
cd "/Users/fabiotakwara/Documents/GitHub/Takwara-Tech/Chatbot - Takwara"

# Ative o ambiente virtual
source .venv/bin/activate
Você saberá que funcionou quando vir (.venv) no início da linha de comando.

Passo 2: Realizar Alterações

Esta é a fase criativa. Edite os ficheiros conforme necessário:

Altere o conteúdo dos artigos (ficheiros .md).
Ajuste a estrutura do site no mkdocs.yml.
Modifique o código das APIs nas suas respectivas pastas.
Passo 3: Testar o Site Localmente

Antes de publicar, pré-visualize sempre as suas alterações visuais:

Bash

# Inicie o servidor de desenvolvimento local
python -m mkdocs serve
Abra o seu navegador e visite http://127.0.0.1:8000. Verifique se tudo está como esperado. Para parar o servidor, volte ao terminal e pressione Ctrl + C.

Passo 4: Atualizar a Base de Conhecimento da AVT (Opcional)

Execute este passo apenas se você alterou ou adicionou ficheiros (.md, .py, .txt) que a AVT precisa de conhecer.

Bash

# Entre na pasta da API
cd backend-api

# Execute o script para recriar a base de dados vetorial
python create_vector_store.py

# Volte para a pasta principal
cd ..
Passo 5: Salvar e Sincronizar com o GitHub (O Ritual)

Este é o ritual para salvar o seu progresso de forma segura no repositório.

Bash

# Adicione todas as suas alterações para serem registadas
git add .

# Crie um "pacote" com uma descrição clara do que foi feito
git commit -m "Ex: Adiciona documentação sobre o forno ecológico"

# Envie o seu trabalho para o GitHub
git push
Passo 6: Publicar as Atualizações para o Mundo (Deploy)

Este é o passo final para que o público veja as suas atualizações. Execute apenas o comando relevante para o que você alterou.

A) Para atualizar o SITE (se alterou o conteúdo ou mkdocs.yml):

Bash

python -m mkdocs gh-deploy
B) Para atualizar a API DA AVT (se executou o Passo 4):

Bash

gcloud functions deploy chatbot-api \
  --gen2 \
  --runtime=python311 \
  --region=southamerica-east1 \
  --source=./backend-api \
  --entry-point=chatbot_api \
  --trigger-http \
  --allow-unauthenticated \
  --memory=512MiB \
  --timeout=300s
Após alguns minutos, as suas atualizações estarão no ar.

# Evolução e Arquitetura do Projeto

Arquitetura da Solução Final
O projeto é dividido em duas componentes principais: o Frontend, responsável pela apresentação do site e pela interface do utilizador, e o Backend, que abriga a inteligência da assistente virtual.

1. Backend: A Assistente Virtual (AVT)
A AVT é uma API "serverless" (sem servidor) publicada na Google Cloud que utiliza um sistema de Busca Aumentada por Geração (RAG) para fornecer respostas contextuais.

Plataforma: Google Cloud Function (Geração 2, Python 3.11, 512MB de memória) na região southamerica-east1.
Stack de IA:
Orquestração: Langchain
Modelo de Linguagem (LLM): Google Generative AI (Gemini 1.5 Flash)
Base de Dados Vetorial: ChromaDB
Ficheiros Essenciais (/backend-api):
create_vector_store.py: Script responsável por clonar o repositório, dividir os documentos (.md, .py, .txt) usando MarkdownHeaderTextSplitter para manter o contexto estrutural e criar uma base de dados vetorial (chroma_db/).
main.py: O código da API. Recebe uma pergunta, usa um MultiQueryRetriever para fazer uma busca abrangente na base vetorial e, com a ajuda de um PromptTemplate customizado, gera uma resposta cordial e contextualizada.
requirements.txt: Lista minimalista de dependências Python essenciais para o funcionamento da API na nuvem.
.env: Ficheiro local para armazenar a chave GOOGLE_API_KEY durante o desenvolvimento.
2. Frontend: O Portal de Documentação
O site é gerado estaticamente com MkDocs, permitindo que seja hospedado gratuitamente e com eficiência no GitHub Pages.

Tecnologia: MkDocs com o tema Material for MkDocs.
Estrutura e Layout:
Layout de 3 Colunas: A aparência foi customizada via CSS (custom.css) para exibir uma estrutura de 3 colunas: navegação principal fixa à esquerda, conteúdo no centro e o índice do artigo à direita.
Navegação e Estrutura: O ficheiro mkdocs.yml define toda a estrutura de navegação (menus e submenus), aparência e extensões do site.
Customização Avançada: Foram usados "overrides" (overrides/partials/footer.html) para modificar componentes do tema, como o rodapé, permitindo a integração de informações de licenciamento e widgets externos.
Fluxo de Trabalho e Manutenção
O ciclo de atualização do projeto segue os seguintes passos:

Preparar Ambiente: Ativar o ambiente virtual Python (source .venv/bin/activate).
Fazer Alterações: Modificar o conteúdo (.md), o código da API ou a configuração do site (mkdocs.yml).
Testar o Site Localmente: Executar python -m mkdocs serve para pré-visualizar as alterações no site em http://127.0.0.1:8000.
Atualizar a Memória da AVT (se necessário): Se o conteúdo dos documentos foi alterado, navegar para backend-api/ e executar python create_vector_store.py para reconstruir a base de dados vetorial.
Publicar Alterações:
Salvar no GitHub: git add ., git commit -m "descrição" e git push.
Publicar Site: Executar python -m mkdocs gh-deploy para atualizar o site no GitHub Pages.
Publicar API: Navegar para backend-api/ e executar o comando gcloud functions deploy chatbot-api ... para atualizar a API na nuvem com a nova base de conhecimento.
Histórico de Desafios e Soluções (Debugging)
A estabilização do projeto envolveu a resolução de uma cascata de problemas interligados que abrangiam todas as camadas da aplicação.

Fase 1: Estabilização da Infraestrutura e da API
Problema: Falha no Deploy (Container Healthcheck Failed).

Diagnóstico: O erro era causado por "poluição de dependências". O requirements.txt da API continha bibliotecas do MkDocs, que eram incompatíveis com o ambiente da Google Cloud.
Solução: Criação de um requirements.txt exclusivo e minimalista para a API, contendo apenas as dependências essenciais.
Problema: API "congelava" e retornava erro de Timeout (300-504s).

Diagnóstico: A investigação revelou múltiplas causas raiz sequenciais:
Memória Insuficiente: A alocação padrão de 256MB era insuficiente para carregar as bibliotecas de IA, causando um "crash" silencioso.
Permissões de IAM: A API não tinha permissão para aceder aos serviços de IA do Google.
Base de Dados Corrompida: O ponto de falha final era o "congelamento" na função de busca (retriever.get_relevant_documents). A base de dados chroma_db estava ineficiente ou corrompida.
Solução:
A memória da função foi aumentada para 512MB.
Foram atribuídos os papéis de IAM "Usuário do Vertex AI" e "Cloud Build Builder" ao Service Account da função.
O processo de criação da base de dados foi refeito do zero, e o script create_vector_store.py foi otimizado.
Problema: Base de conhecimento da AVT estava desatualizada.

Diagnóstico: Um ficheiro .gcloudignore na pasta da API continha a linha chroma_db/, impedindo que a base de dados atualizada fosse enviada para a nuvem durante o deploy.
Solução: A linha chroma_db/ foi removida do ficheiro .gcloudignore.
Fase 2: Aprimoramento da Inteligência e da Experiência do Utilizador
Com a infraestrutura estável, o foco mudou para o refinamento da funcionalidade e da experiência.

Objetivo: Tornar a AVT mais inteligente e contextual.

Implementação:
Otimização dos Dados: Foi adotado o MarkdownHeaderTextSplitter, que divide os documentos com base na sua estrutura de títulos, criando "pedaços" de conhecimento mais coesos.
Busca Avançada: O retriever padrão foi substituído pelo MultiQueryRetriever, que reformula a pergunta do utilizador de várias maneiras para realizar uma busca mais ampla e precisa.
Engenharia de Prompt: Foi criado um PromptTemplate detalhado para dar à AVT uma persona, instruções de comportamento (ser cordial, responder em português, citar fontes) e um guião sobre como agir quando não encontra uma resposta.
Objetivo: Implementar um layout customizado e profissional.

Implementação: O layout padrão foi completamente modificado usando CSS Grid e Flexbox, e o rodapé foi personalizado com overrides do MkDocs para refletir a identidade visual e os objetivos do projeto Takwara Tech.