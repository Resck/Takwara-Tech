# Documentação Técnica do Projeto Takwara-Tech: Plataforma GitHub, Sistema de Documentação e API de Inteligência Artificial

Este documento consolida informações técnicas sobre a configuração, o fluxo de trabalho de desenvolvimento, o histórico de depuração e o estado atual da plataforma web do projeto Takwara-Tech, hospedada no GitHub e alimentada por uma API de Inteligência Artificial. O objetivo é fornecer uma visão abrangente da arquitetura implementada e dos desafios superados.

## Índice

*   [Documentação Técnica do Projeto Takwara-Tech: Plataforma GitHub, Sistema de Documentação e API de Inteligência Artificial](#documentação-técnica-do-projeto-takwara-tech-plataforma-github-sistema-de-documentação-e-api-de-inteligência-artificial)
*   [Seção 1: Introdução ao Ecossistema Takwara-Tech no GitHub](#seção-1-introdução-ao-ecossistema-takwara-tech-no-github)
    *   [1.1. Componentes da Plataforma](#11-componentes-da-plataforma)
    *   [1.2. Visão Estratégica da Interface](#12-visão-estratégica-da-interface)
*   [Seção 2: O Ciclo de Desenvolvimento e Publicação](#seção-2-o-ciclo-de-desenvolvimento-e-publicação)
    *   [2.1. Gerenciamento de Conteúdo e Configuração](#21-gerenciamento-de-conteúdo-e-configuração)
    *   [2.2. Processamento da Base de Conhecimento da IA (`create_vector_store.py`)](#22-processamento-da-base-de-conhecimento-da-ia-create_vector_storepy)
    *   [2.3. Fluxo de Publicação (Deploy)](#23-fluxo-de-publicação-deploy)
*   [Seção 3: Histórico Cronológico de Desenvolvimento e Depuração](#seção-3-histórico-cronológico-de-desenvolvimento-e-depuração)
    *   [3.1. Estabilização Inicial da Infraestrutura e API Backend](#31-estabilização-inicial-da-infraestrutura-e-api-backend)
        *   [Fase 1: Erros Iniciais no Frontend](#fase-1-erros-iniciais-no-frontend)
        *   [Fase 2: Problema de CORS](#fase-2-problema-de-cors)
        *   [Fase 3: Colapso por Falta de Memória](#fase-3-colapso-por-falta-de-memória)
        *   [Fase 4: Timeout e Permissões de IAM](#fase-4-timeout-e-permissões-de-iam)
        *   [Fase 5: Ponto de Falha Final - Busca na Base de Dados](#fase-5-ponto-de-falha-final---busca-na-base-de-dados)
    *   [3.2. Refinamento da Inteligência da Assistente Virtual (AVT)](#32-refinamento-da-inteligência-da-assistente-virtual-avt)
    *   [3.3. Implementação e Desafios de Layout da Interface](#33-implementação-e-desafios-de-layout-da-interface)
        *   [Visão Estratégica do Layout](#visão-estratégica-do-layout)
        *   [Histórico de Implementação e Diagnóstico (Tentativas)](#histórico-de-implementação-e-diagnóstico-tentativas)
        *   [Implementação da Solução com Web Components](#implementação-da-solução-com-web-components)
*   [Seção 4: Estado Atual, Pendências e Próximas Etapas](#seção-4-estado-atual-pendências-e-próximas-etapas)
    *   [4.1. Estado Atual Implementado](#41-estado-atual-implementado)
    *   [4.2. Pendências Críticas](#42-pendências-críticas)
    *   [4.3. Plano de Ação e Roadmap](#43-plano-de-ação-e-roadmap)
*   [Seção 5: Apêndice Técnico: Análise Detalhada do Script `create_vector_store.py`](#seção-5-apêndice-técnico-análise-detalhada-do-script-create_vector_storepy)
    *   [5.1. Objetivo do Script](#51-objetivo-do-script)
    *   [5.2. O Fluxo de Trabalho: Uma Jornada em 6 Etapas](#52-o-fluxo-de-trabalho-uma-jornada-em-6-etapas)
    *   [5.3. Destrinchando o Código](#53-destrinchando-o-código)
*   [Seção 6: Referências e Links](#seção-6-referências-e-links)

## Seção 1: Introdução ao Ecossistema Takwara-Tech no GitHub

O portal do projeto Takwara-Tech, hospedado no GitHub Pages ([https://resck.github.io/Takwara-Tech/](https://resck.github.io/Takwara-Tech/)), representa uma plataforma de documentação e interação focada em soluções sustentáveis com bambu. A plataforma combina um site estático com uma API de Inteligência Artificial para fornecer informações e ferramentas aos usuários.

### 1.1. Componentes da Plataforma

O ecossistema técnico é composto por três elementos principais:

*   **Frontend:** O site estático, gerado utilizando o MkDocs e o tema Material for MkDocs. Contém a documentação do projeto em arquivos Markdown e implementa a interface do usuário, incluindo a integração com a Assistente Virtual (AVT) e outras ferramentas.
*   **Backend/API:** Uma API desenvolvida em Python 3.11 e implantada como uma Google Cloud Function (Geração 2) na região `southamerica-east1`. Esta API utiliza uma stack de IA (Langchain, Google Generative AI, ChromaDB) para processar as consultas da Assistente Virtual, realizando busca de similaridade em uma base de conhecimento vetorial gerada a partir do conteúdo do site.
*   **Base de Conhecimento da IA (`chroma_db`):** Uma base de dados vetorial local, gerada a partir do conteúdo textual (Markdown, Python, TXT) do repositório do site. Esta base de dados é utilizada pela API backend para responder a perguntas contextuais.

### 1.2. Visão Estratégica da Interface

O objetivo final da interface do portal é evoluir para além de um simples repositório de documentos estáticos, transformando-o numa plataforma de interação e dados em tempo real. A visão estratégica para o layout e funcionalidade inclui:

*   **Arquitetura da Interface:** Um layout que apresente de forma clara e persistente uma navegação principal do site (índice geral), uma área central focada no conteúdo (artigos) e uma "Tool Box Interativa" sempre acessível, contendo as ferramentas da plataforma (Assistente Virtual, Grafo de Conhecimento, Calculadoras). Um índice de conteúdo para a página que está a ser lida (TOC - Table of Contents) também deve estar presente.
*   **Painel de Impacto (Cabeçalho e Rodapé):** O cabeçalho e o rodapé devem ser customizados para incluir "instrumentos indicadores" — APIs que exibem dados ambientais e sociais em tempo real (ex: "Climate Clock", níveis de CO₂, dados de queimadas, etc.).
*   **Comportamento da AVT:** A Assistente Virtual Takwara (AVT) deve ter uma busca contextual, priorizando a pesquisa na página em que o utilizador se encontra antes de realizar uma busca global no repositório.

## Seção 2: O Ciclo de Desenvolvimento e Publicação

Manter a plataforma atualizada com novo conteúdo e funcionalidades requer um fluxo de trabalho bem definido, que integra a gestão de código, a atualização da base de conhecimento da IA e a publicação do site estático e da API backend.

### 2.1. Gerenciamento de Conteúdo e Configuração

*   **Conteúdo:** O conteúdo textual do site é escrito e mantido em arquivos Markdown (`.md`) localizados dentro da pasta `docs/` do repositório.
*   **Configuração do Site:** O arquivo `mkdocs.yml` na raiz do repositório controla a estrutura do site, navegação, tema e plugins. É crucial "matricular" novos artigos na seção `nav:` deste arquivo para que sejam incluídos no menu de navegação e processados pelo MkDocs.
*   **Exclusão de Arquivos Temporários:** O arquivo `.gitignore` deve ser configurado para excluir pastas geradas automaticamente e arquivos temporários que não devem ser versionados ou enviados para o repositório fonte ou incluídos no deploy do backend. As seguintes linhas são essenciais:
    ```gitignore
    /site/
    /Chatbot - Takwara/temp_repo/
    /backend-api/chroma_db/ # Certificar que a base de dados não é versionada com o código fonte da API
    ```

### 2.2. Processamento da Base de Conhecimento da IA (`create_vector_store.py`)

O script `create_vector_store.py` é o "indexador" da Assistente Virtual. Sua função é ler o conteúdo relevante do repositório, processá-lo e gerar a base de dados vetorial (`chroma_db`).

*   **Objetivo:** Ler todo o conteúdo textual relevante (`.py`, `.md`, `.txt`) do repositório, processá-lo com modelos de IA (embeddings) e salvar este conhecimento de forma estruturada em uma base de dados vetorial local (ChromaDB). Esta base de dados alimenta a API backend para buscas semânticas rápidas.
*   **Fluxo de Trabalho do Script:**
    1.  **Clonar:** Baixa uma cópia do repositório do GitHub para uma pasta temporária local (`./temp_repo`).
    2.  **Carregar:** Lê os arquivos de texto especificados pelo filtro.
    3.  **Dividir:** Quebra documentos longos em pedaços menores e sobrepostos para otimizar o processamento pela IA, utilizando ferramentas como `RecursiveCharacterTextSplitter` ou `MarkdownHeaderTextSplitter` (para priorizar a estrutura de títulos).
    4.  **Vetorizar (Embed):** Envia cada pedaço de texto para a API de Embeddings do Google (utilizando `GoogleGenerativeAIEmbeddings`) para convertê-los em vetores numéricos que representam seu significado semântico.
    5.  **Armazenar:** Guarda cada pedaço de texto (documento) junto com seu vetor correspondente em uma base de dados local (`ChromaDB`).
    6.  **Salvar:** Persiste a base de dados no disco, em um diretório especificado (`./backend-api/chroma_db`), para que a API backend possa acessá-la.
*   **Execução:** O script é executado via linha de comando no terminal:
    ```bash
    python create_vector_store.py
    ```
    (É necessário ter um arquivo `.env` com a chave `GOOGLE_API_KEY` configurada no ambiente).

### 2.3. Fluxo de Publicação (Deploy)

O ciclo de atualização da plataforma envolve uma sequência de passos para garantir que as alterações no conteúdo, na base de conhecimento da IA e no código da API sejam refletidas no site publicado.

*   **Fluxo de Atualização (SOP):**
    1.  **Edição de Conteúdo:** Crie ou edite os arquivos Markdown (`.md`) em `docs/`. Se for um novo arquivo, adicione-o à navegação no `mkdocs.yml`.
    2.  **Atualização da Base de Conhecimento da IA:**
        *   Execute o script `create_vector_store.py` para gerar a nova base de dados vetorial, salvando-a *dentro* do diretório da API (`./backend-api/chroma_db/`).
        *   Verifique se o `.gitignore` da API *não* impede que a pasta `chroma_db` seja incluída no deploy da função.
    3.  **Deploy da API Backend:** Envie a nova versão da Google Cloud Function, incluindo a base de dados atualizada:
        ```bash
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
        ```
    4.  **Salve e Versiona as Alterações no Git:**
        *   Adicione todas as suas alterações locais (arquivos de conteúdo, `mkdocs.yml`, arquivos da API *com a nova base de dados*, etc.):
            ```bash
            git add .
            ```
        *   Crie um commit para registrar oficialmente as alterações com uma mensagem descritiva:
            ```bash
            git commit -m "Mensagem descrevendo as atualizações (ex: Adiciona novo artigo sobre tratamento de bambu e atualiza IA)"
            ```
    5.  **Publique o Site Frontend:** Execute o comando do MkDocs que constrói o site estático e o publica no GitHub Pages (geralmente no branch `gh-pages`). Este comando utiliza o último commit do branch principal (`main`) como base:
        ```bash
        mkdocs gh-deploy
        ```
    6.  **Verificação Final:** Aguarde alguns minutos (2-3) para a propagação do deploy. Abra o site online ([https://resck.github.io/Takwara-Tech/](https://resck.github.io/Takwara-Tech/)) em uma janela anônima ou limpe o cache do navegador para garantir que está vendo a versão mais recente.

## Seção 3: Histórico Cronológico de Desenvolvimento e Depuração

O desenvolvimento da plataforma envolveu a superação de diversos desafios técnicos complexos, desde a configuração inicial da infraestrutura na nuvem até o refinamento da inteligência da Assistente Virtual e os desafios de customização da interface. Este seção documenta o percurso de depuração e evolução.

### 3.1. Estabilização Inicial da Infraestrutura e API Backend

O processo de colocar a API backend em funcionamento e garantir que se comunicasse corretamente com o frontend e os serviços de IA do Google envolveu a depuração de uma série de problemas interligados.

#### Fase 1: Erros Iniciais no Frontend

*   **Sintomas:** Erros 404 ao tentar carregar imagens (logo), layout quebrado no site publicado, e erros de `SyntaxError` em arquivos JavaScript que impediam a renderização do chatbot e da calculadora no navegador do usuário.
*   **Diagnóstico:** Caminhos de arquivos incorretos referenciados no `mkdocs.yml` e conteúdo inválido (texto não-código) introduzido acidentalmente na primeira linha de alguns arquivos JavaScript.
*   **Solução:** Limpeza dos arquivos JavaScript corrompidos e correção dos caminhos de arquivos (links para imagens, scripts) no `mkdocs.yml`.
*   **Resultado:** A interface visual do site foi restaurada no navegador, mas a área do chatbot ainda apresentava um "erro de comunicação" com o backend.

#### Fase 2: Problema de CORS

*   **Sintomas:** A consola do navegador exibia consistentemente o erro de segurança `blocked by CORS policy` (Política CORS bloqueou a requisição). Não havia registros de atividade nos logs da Google Cloud Function para essas requisições bloqueadas pelo navegador.
*   **Diagnóstico:** O navegador estava bloqueando as requisições do site estático (frontend) para a API backend porque a API não retornava os cabeçalhos de permissão `Access-Control-Allow-Origin` necessários.
*   **Solução:** Tentativa inicial de implementar a lógica de CORS no código da API utilizando a biblioteca `Flask-Cors`.
*   **Resultado:** O problema de CORS no navegador persistiu, indicando que a função na nuvem sequer estava conseguindo iniciar e executar o código de configuração do CORS antes de colapsar.

#### Fase 3: Colapso por Falta de Memória

*   **Sintomas:** O erro de CORS não era a causa raiz, mas um sintoma de um problema mais profundo. Uma análise detalhada dos logs da Google Cloud Function revelou o erro fatal: `Memory limit... exceeded` (Limite de memória excedido).
*   **Diagnóstico:** A Google Cloud Function, com sua configuração padrão de 256MB de memória, era insuficiente para carregar e inicializar as bibliotecas de Inteligência Artificial (`Langchain`, `ChromaDB`, etc.) necessárias para a API. Isso causava o "colapso" imediato da função ao tentar iniciar.
*   **Solução:** A memória alocada para a função foi aumentada para 512MiB utilizando o parâmetro `--memory=512MiB` no comando de deploy (`gcloud functions deploy`).
*   **Resultado:** A função na nuvem tornou-se estável, deixou de colapsar no arranque e começou a responder aos pedidos iniciais (`OPTIONS`) com status `200 OK`. No entanto, o erro de CORS no navegador, de forma inesperada, continuou a ocorrer para as requisições principais (`POST`).

#### Fase 4: Timeout e Permissões de IAM

*   **Sintomas:** Testes diretos à API utilizando ferramentas como `curl` (que ignoram as políticas de CORS do navegador) mostraram que as requisições eram enviadas com sucesso, mas a API nunca respondia com o resultado da consulta, causando um timeout após o tempo limite configurado (300 segundos).
*   **Diagnóstico:** O "congelamento" da execução estava ocorrendo *dentro* do código da função após o seu início bem-sucedido. A principal suspeita recaiu sobre a chamada a serviços externos, especificamente a API de IA do Google (Gemini-Pro), provavelmente devido à falta de permissões de acesso para a conta de serviço da função.
*   **Solução:** Foram adicionados manualmente os papéis de IAM (Identity and Access Management) necessários à conta de serviço associada à Cloud Function (`...-compute@developer.gserviceaccount.com`) através da consola do Google Cloud: "Usuário do Vertex AI" (para permitir o uso dos modelos de IA do Google) e "Cloud Build Builder" (para resolver um problema secundário identificado no processo de build/deploy).
*   **Resultado:** Todas as permissões de infraestrutura e acesso foram corrigidas, mas o timeout de 300 segundos durante as requisições principais persistiu.

#### Fase 5: Ponto de Falha Final - Busca na Base de Dados

*   **Sintomas:** O timeout de 300 segundos persistia mesmo com todas as configurações de infraestrutura e permissões aparentemente corretas.
*   **Diagnóstico:** Foi implantada uma versão da API com logs de depuração detalhados no código Python ("PASSO 1", "PASSO 2", etc.). Os logs provaram inequivocamente que a execução iniciava, carregava as bibliotecas e a base de dados, imprimia "PASSO 1" (antes da busca), mas depois "congelava" indefinidamente na chamada específica responsável por fazer a busca de similaridade na base de dados vetorial ChromaDB: `qa_chain.retriever.get_relevant_documents(query)`.
*   **Solução Proposta:** A hipótese levantada foi que a própria base de dados `chroma_db` estava corrompida ou ineficiente para o ambiente de execução, ou havia uma incompatibilidade entre a versão da base de dados e as bibliotecas no ambiente da Cloud Function. A solução aplicada foi apagar o diretório `chroma_db` local, recriá-lo do zero executando novamente o script `create_vector_store.py` (garantindo que salvava na pasta correta para o deploy) e realizar um novo deploy completo da função.
*   **Resultado:** Esta etapa **resolveu o bloqueio principal**. A execução da busca na base de dados deixou de congelar, e a API passou a responder com os resultados da busca (embora as respostas iniciais ainda fossem genéricas, o que levou à próxima fase de depuração).

### 3.2. Refinamento da Inteligência da Assistente Virtual (AVT)

Com a API estável e respondendo, a próxima fase foi melhorar a qualidade e relevância das respostas da Assistente Virtual (AVT), que ainda parecia não utilizar plenamente o conteúdo disponível.

*   **Desafio:** A AVT estava funcional, mas suas respostas eram genéricas, frequentemente afirmando não encontrar informação que sabíamos existir na base de conhecimento.
*   **Soluções Implementadas:**
    *   **Otimização da Quebra de Documentos:** O script `create_vector_store.py` foi aprimorado para utilizar o `MarkdownHeaderTextSplitter`. Esta ferramenta divide os documentos Markdown com base em sua estrutura de títulos (`#`, `##`, etc.), criando "pedaços" de conhecimento ("chunks") mais curtos, mais ricos em contexto (cada pedaço contém o título e subtítulos que o precedem) e, consequentemente, mais fáceis para a IA encontrar informações relevantes durante a busca.
    *   **Upgrade do Retriever:** Implementamos o `MultiQueryRetriever` na API backend. Esta técnica permite que a IA reformule a pergunta original do usuário de várias formas diferentes antes de realizar a busca na base de dados vetorial. Isso aumenta a chance de encontrar documentos relevantes, mesmo que a formulação inicial do usuário não seja perfeita. Os parâmetros do retriever foram ajustados (afinados) para aumentar a quantidade de resultados retornados e a tolerância da busca por similaridade.
    *   **Engenharia de Prompt:** Criamos um `PromptTemplate` customizado. Este template define a "persona" da AVT (uma assistente virtual informativa da Takwara-Tech), estabelece seu tom de comunicação (cordial, prestativa), define suas regras de comportamento (sempre citar as fontes/documentos que utilizou para gerar a resposta, responder no idioma do usuário que enviou a pergunta, lidar graciosamente com erros de digitação) e fornece contexto adicional para a IA gerar respostas mais úteis e direcionadas.

### 3.3. Implementação e Desafios de Layout da Interface

Em paralelo à estabilização e refinamento da API, foram realizadas diversas tentativas para implementar a visão estratégica do layout do portal, focando na "Tool Box Interativa".

#### Visão Estratégica do Layout

*   Uma navegação principal (índice geral) fixa.
*   Uma área central para o conteúdo dos artigos.
*   Uma "Tool Box Interativa" fixa, contendo a AVT, o Grafo de Conhecimento e calculadoras.
*   Um índice de conteúdo da página atual (TOC).
*   Integração de "Painéis de Impacto" (dados em tempo real) no cabeçalho e rodapé.

#### Histórico de Implementação e Diagnóstico (Tentativas)

Para alcançar esta visão utilizando o tema Material for MkDocs, que possui uma estrutura de layout própria baseada em CSS Grid, foram testadas várias abordagens de customização:

*   **Tentativa 1: Abordagem com CSS Grid Diretamente:**
    *   **Ação:** Aplicação direta de regras CSS `display: grid` e `grid-template-columns` para definir as colunas desejadas no contêiner principal do tema (`.md-grid`).
    *   **Resultado:** O layout de múltiplas colunas funcionou corretamente apenas na página inicial. Em outras páginas (artigos), a estrutura HTML gerada pelo tema diferia sutilmente, resultando em quebras de layout e "encavalamento" (sobreposição) de elementos.
*   **Tentativa 2: Abordagem com Template Override (`main.html`):**
    *   **Ação:** Tentativa de obter controle total sobre a estrutura da página substituindo o conteúdo do arquivo `overrides/main.html` por uma estrutura de colunas customizada (`div`s com classes CSS).
    *   **Resultado:** Conflitos de layout ainda mais severos ocorreram. A substituição completa do bloco de conteúdo principal do tema (`{% block content %}`) quebrou a lógica interna e os scripts do tema, que dependem da estrutura original de divs e classes, resultando na perda da coluna de conteúdo e na duplicação de elementos de navegação.
*   **Diagnóstico do Problema:** As tentativas de forçar um layout de múltiplas colunas fixas através de manipulação direta do CSS ou override completo do template de conteúdo (`main.html`) entram em conflito fundamental com a arquitetura e o CSS do tema Material for MkDocs. O tema foi projetado para gerenciar dinamicamente a posição e o comportamento de seus três componentes principais (navegação primária, conteúdo principal e índice da página) em diferentes tamanhos de tela, e tentar introduzir uma quarta coluna fixa ou reestruturar completamente o HTML do conteúdo causa instabilidade.

#### Implementação da Solução com Web Components

Diante da resiliência do tema padrão à manipulação direta do layout, a estratégia foi pivotada para uma solução mais robusta e isolada tecnologicamente.

*   **Solução Definida:** Implementar a "Tool Box Interativa" utilizando a tecnologia de **Web Components**.
*   **Ação:**
    1.  Criação de um elemento HTML customizado (`<takwara-toolbox>`).
    2.  Utilização do **Shadow DOM** dentro deste Web Component. Esta técnica cria um DOM (Document Object Model) e um escopo de estilos isolados ("firewall") para a Tool Box, impedindo que o CSS do tema principal afete o layout da Tool Box e, crucialmente, impedindo que o CSS da Tool Box conflite com o layout do tema.
    3.  Implementação da lógica de posicionamento em JavaScript (`toolbox.js`). Este script calcula dinamicamente a altura do cabeçalho e rodapé do site e ajusta a altura da Tool Box para preencher o espaço vertical disponível, fixando-a à esquerda. A lógica também gerencia o comportamento de "encolhimento" da Tool Box conforme o usuário rola a página, garantindo que ela não sobreponha o rodapé.
*   **Resultado:** Esta abordagem com Web Components **resolveu os conflitos de layout**. A "Takwara Tool Box" é renderizada com sucesso como um componente isolado, fixo à esquerda, com altura dinâmica e comportamento de scroll correto. O layout geral do site permanece estável, consistente e responsivo, sem quebras ou sobreposições causadas pela Tool Box. A estrutura HTML para as ferramentas (AVT, Grafo, Calculadora) é carregada corretamente dentro do Web Component.

## Seção 4: Estado Atual, Pendências e Próximas Etapas

Com base no trabalho realizado, a plataforma atingiu um estado de estabilidade funcional e estrutural, mas ainda possui pendências que requerem desenvolvimento.

### 4.1. Estado Atual Implementado (Junho de 2025)

*   **Infraestrutura e API:** A API backend está implantada, estável e acessível na Google Cloud Function. Problemas de deploy, memória e permissões foram resolvidos. A comunicação básica entre frontend e backend está funcional.
*   **Base de Conhecimento da IA:** O script `create_vector_store.py` está otimizado para quebrar documentos de forma contextual (usando `MarkdownHeaderTextSplitter`) e gerar a base de dados `chroma_db` corretamente.
*   **Inteligência da AVT:** A Assistente Virtual utiliza o `MultiQueryRetriever` e um `PromptTemplate` customizado para gerar respostas mais relevantes e contextualizadas a partir da base de conhecimento. Ela cita as fontes encontradas.
*   **Layout Básico da Tool Box:** A estrutura visual da "Takwara Tool Box" está implementada como um Web Component isolado e fixo à esquerda, com posicionamento e comportamento de scroll dinâmicos, sem conflitos de layout com o tema principal. O HTML básico das ferramentas está carregado dentro dela.
*   **Customização Básica do Tema:** O menu de navegação principal está configurado como barra lateral fixa. Um rodapé customizado, incluindo um widget de relógio climático (`Climate Clock`), foi implementado via override de template.

### 4.2. Pendências Críticas

*   **Ativação da Lógica das Ferramentas na Tool Box:** Embora a estrutura HTML das ferramentas (AVT, Grafo de Conhecimento, Calculadoras) esteja presente dentro da Tool Box, os scripts JavaScript que controlam a lógica e a interatividade de cada ferramenta (por exemplo, o script que gerencia o formulário de chat, o grafo interativo, as calculadoras) não estão a conseguir inicializar corretamente.
    *   **Diagnóstico:** A causa mais provável é uma "race condition". Os scripts das ferramentas são carregados e tentam inicializar-se quando a página principal carrega (evento `DOMContentLoaded`), mas o HTML específico das ferramentas só é adicionado ao DOM *depois*, quando o Web Component `<takwara-toolbox>` é criado e renderiza seu conteúdo. Os scripts não encontram os elementos HTML que esperam e falham ao anexar seus "event listeners" (ex: ao botão de enviar mensagem do chat).
*   **Implementação Completa das APIs de Monitoramento:** A integração dos "Painéis de Impacto" no cabeçalho e rodapé, exibindo dados em tempo real (CO₂, temperatura, etc.), ainda não foi iniciada.
*   **Ajustes Finos de Design:** Polimento final do rodapé padrão do tema (que se mostrou resistente a algumas alterações de CSS) e revisão geral da UI/UX após a implementação de todas as funcionalidades.
*   **Busca Contextual da AVT (Nível de Página):** A lógica para a AVT priorizar a busca na página específica em que o usuário se encontra (contexto da URL atual) antes de fazer uma busca global na base de conhecimento ainda precisa ser implementada no código da API.

### 4.3. Plano de Ação e Roadmap

As próximas etapas de desenvolvimento focarão em resolver as pendências críticas e realizar a visão completa da plataforma.

1.  **Ativação da Tool Box (Prioridade Máxima):** Implementar um sistema de eventos customizados. O script que gerencia o Web Component (`toolbox.js`), após injetar o HTML das ferramentas no Shadow DOM, irá disparar um evento global customizado (ex: `takwara:tools-ready`). Os scripts individuais das ferramentas (`script.js` do chat, `graph.js`, etc.) serão modificados para "escutar" este evento específico. Eles só tentarão inicializar sua lógica *após* receberem este evento, garantindo que o HTML necessário já esteja presente no DOM isolado do Web Component.
2.  **Implementação do "Painel de Impacto":** Integrar as APIs de dados para popular o painel customizado no cabeçalho e rodapé. Definir o primeiro indicador a ser implementado (ex: Níveis de CO₂) e desenvolver a lógica para buscar e exibir esses dados em tempo real.
3.  **Refinamento da Inteligência da AVT (Busca Contextual):** Modificar o código da API backend para receber a URL da página atual como um parâmetro na requisição do frontend. Utilizar esta URL para carregar o conteúdo específico da página e dar maior peso a este texto durante a busca por similaridade na base de dados vetorial, permitindo que a AVT responda de forma mais relevante ao conteúdo que o usuário está visualizando.
4.  **Polimento Final e UI/UX:** Realizar ajustes de design no rodapé e em outras áreas que apresentaram resistência a customizações CSS. Conduzir uma revisão geral da interface do usuário e experiência do usuário após a integração de todas as funcionalidades.
5.  **Implementação Completa das Ferramentas:** Finalizar a lógica e a integração das demais ferramentas planejadas (Grafo de Conhecimento, Calculadoras) dentro da Tool Box.

## Seção 5: Apêndice Técnico: Análise Detalhada do Script `create_vector_store.py`

Este apêndice fornece uma análise aprofundada do script Python responsável por gerar a base de conhecimento da Assistente Virtual.

### 5.1. Objetivo do Script

O `create_vector_store.py` funciona como um "indexador" ou "construtor de memória" para a Assistente Virtual. Sua missão principal é:

1.  Acessar o conteúdo textual de um repositório Git (especificamente o repositório do site Takwara-Tech).
2.  Processar esse conteúdo utilizando modelos de Embedding (IA).
3.  Salvar o texto original e seus vetores correspondentes em uma base de dados vetorial local.

Esta base de dados (ChromaDB) é o que a API backend utiliza para realizar buscas rápidas de similaridade semântica, permitindo que a Assistente Virtual encontre informações relevantes para responder às perguntas dos usuários, mesmo que as palavras exatas da pergunta não estejam presentes no texto original.

### 5.2. O Fluxo de Trabalho: Uma Jornada em 6 Etapas

Antes de analisar o código, é útil entender a sequência lógica de operações realizadas pelo script:

1.  **Clonar:** O script inicia baixando uma cópia local do repositório Git alvo (definido pela `REPO_URL`) para um diretório temporário (`./temp_repo`).
2.  **Carregar:** Ele lê os arquivos de texto baixados que correspondem a um filtro especificado (por exemplo, apenas arquivos `.py`, `.md`, `.txt`).
3.  **Dividir:** Como modelos de Embedding geralmente têm um limite no tamanho do texto que podem processar de uma vez, e para garantir que os resultados da busca sejam granulars e contextuais, o script quebra os documentos lidos em pedaços menores (chunks) com alguma sobreposição entre eles. Ferramentas como `RecursiveCharacterTextSplitter` ou `MarkdownHeaderTextSplitter` são usadas para essa divisão inteligente.
4.  **Vetorizar (ou "Embed"):** Para cada pedaço de texto resultante da divisão, o script envia este texto para uma API de modelo de Embedding (neste caso, a API do Google, `GoogleGenerativeAIEmbeddings`). O modelo de IA processa o texto e o converte em um vetor numérico de alta dimensão (um "embedding") que captura seu significado semântico. Textos com significados similares terão vetores próximos no espaço multidimensional.
5.  **Armazenar:** O script armazena cada pedaço de texto original juntamente com seu vetor correspondente em uma base de dados vetorial (ChromaDB). Esta base de dados é otimizada para realizar buscas rápidas de vizinhos mais próximos (ou seja, encontrar vetores - e, portanto, textos - semanticamente similares a um vetor de consulta).
6.  **Salvar:** Finalmente, o script salva a base de dados ChromaDB criada no disco, em um diretório persistente (definido por `PERSIST_DIRECTORY`, configurado para ser `./backend-api/chroma_db`). Isso permite que a API backend carregue a base de dados rapidamente sem ter que refazer todo o processo de clonagem, carregamento, divisão e vetorização a cada vez.

### 5.3. Destrinchando o Código

Vamos analisar os blocos de código Python que implementam este fluxo:

#### 1. As Importações (As Ferramentas Necessárias)

```python
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import GitLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# Pode incluir outras importações se o script usar MarkdownHeaderTextSplitter, etc.
# from langchain.text_splitter import MarkdownHeaderTextSplitter
```

*   `import os`: Fornece funções para interagir com o sistema operacional, útil para manipular caminhos de arquivos e diretórios.
*   `from dotenv import load_dotenv`: Importa a função para carregar variáveis de ambiente a partir de um arquivo `.env`, usado para carregar a chave da API do Google sem expô-la no código.
*   `from langchain_community.document_loaders import GitLoader`: Importa a classe `GitLoader` da biblioteca LangChain, especializada em clonar repositórios Git e carregar seu conteúdo como documentos.
*   `from langchain.text_splitter import RecursiveCharacterTextSplitter`: Importa uma classe para dividir textos longos de forma recursiva, tentando manter a coerência contextual. (Outros splitters como `MarkdownHeaderTextSplitter` podem ser usados, dependendo da versão do script).
*   `from langchain_community.vectorstores import Chroma`: Importa a classe `Chroma` da biblioteca LangChain, que fornece a interface para a base de dados vetorial ChromaDB.
*   `from langchain_google_genai import GoogleGenerativeAIEmbeddings`: Importa a classe para criar embeddings usando a API Generative AI do Google (Gemini/Vertex AI).

#### 2. As Configurações Globais (Definindo o Alvo)

```python
load_dotenv() # Carrega variáveis do .env

# Configurações do Repositório e Diretório de Persistência
REPO_URL = "URL_DO_SEU_REPOSITORIO_AQUI" # Ex: "https://github.com/resck/Takwara-Tech.git"
PERSIST_DIRECTORY = "./backend-api/chroma_db" # Diretório onde a base de dados ChromaDB será salva (dentro da pasta da API)
```

*   `load_dotenv()`: Executa a função para ler o arquivo `.env` (que deve conter `GOOGLE_API_KEY="SUA_CHAVE_AQUI"`) e carregar as variáveis para o ambiente do script.
*   `REPO_URL`: Uma variável string que define a URL do repositório Git a ser clonado e processado pelo script.
*   `PERSIST_DIRECTORY`: Define o caminho do diretório onde a base de dados ChromaDB persistirá (será salva). É configurado para apontar para um subdiretório dentro da pasta que será incluída no deploy da API backend, garantindo que a base de dados correta seja enviada.

#### 3. A Função Principal (`build_and_save_vector_store`)

Este é o bloco de código que orquestra as etapas do fluxo de trabalho.

```python
def build_and_save_vector_store():
    # 1. e 2. Clonar e Carregar Documentos
    print(f"Clonando repositório de {REPO_URL}...")
    loader = GitLoader(
        clone_url=REPO_URL,
        repo_path="./temp_repo", # Clona para um diretório temporário
        file_filter=lambda file_path: file_path.endswith((".py", ".md", ".txt")) # Filtra por tipos de arquivo
    )
    docs = loader.load() # Carrega os documentos filtrados

    print(f"Carregados {len(docs)} documentos.")

    # 3. Dividir Documentos em Pedaços (Chunks)
    print("Dividindo documentos em pedaços (chunks)...")
    # Configuração do divisor (pode variar, MarkdownHeaderTextSplitter seria usado para estrutura MD)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # Se usar MarkdownHeaderTextSplitter, seria algo como:
    # headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ...]
    # text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    chunks = text_splitter.split_documents(docs)
    print(f"Criados {len(chunks)} pedaços de texto.")

    # 4. Vetorizar (Embed) os Pedaços
    print("Gerando embeddings para os pedaços (chunks)...")
    # Inicializa o modelo de Embedding do Google
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") # Modelo recomendado para embeddings

    # 5. e 6. Armazenar e Salvar na Base de Dados Vetorial (ChromaDB)
    print(f"Criando e salvando a base de dados vetorial em {PERSIST_DIRECTORY}...")
    # Cria uma nova base de dados ChromaDB a partir dos chunks e embeddings, persistindo no diretório especificado
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )

    # O método from_documents já salva a base de dados no disco
    # vectorstore.persist() # Este método pode ser chamado explicitamente dependendo da versão da biblioteca

    print("Base de dados vetorial criada e salva com sucesso.")

    # Opcional: Limpar o diretório temporário clonado
    # import shutil
    # if os.path.exists("./temp_repo"):
    #     shutil.rmtree("./temp_repo")
    #     print("Diretório temporário ./temp_repo removido.")

if __name__ == "__main__":
    build_and_save_vector_store()
```

*   `def build_and_save_vector_store():`: Define a função principal que contém a lógica de processamento.
*   `loader = GitLoader(...)`: Inicializa o `GitLoader` com a URL do repositório, um caminho temporário para clonagem (`./temp_repo`) e um filtro (`file_filter`) para carregar apenas arquivos de texto relevantes (Python, Markdown, TXT).
*   `docs = loader.load()`: Executa a operação de clonagem e carregamento, armazenando os documentos lidos em uma lista chamada `docs`.
*   `text_splitter = RecursiveCharacterTextSplitter(...)`: Inicializa um objeto divisor de texto (`text_splitter`) com parâmetros para definir o tamanho dos pedaços (`chunk_size`) e a sobreposição entre eles (`chunk_overlap`). O `MarkdownHeaderTextSplitter` seria uma alternativa específica para documentos Markdown.
*   `chunks = text_splitter.split_documents(docs)`: Aplica o divisor aos documentos carregados, gerando uma lista de pedaços menores.
*   `embeddings = GoogleGenerativeAIEmbeddings(...)`: Inicializa o modelo de Embedding do Google a ser utilizado para converter texto em vetores. `models/embedding-001` é um modelo comum para essa tarefa.
*   `vectorstore = Chroma.from_documents(...)`: Este é um passo crucial. Ele cria (ou carrega, se já existir) uma base de dados ChromaDB (`vectorstore`). O método `from_documents` recebe a lista de pedaços (`chunks`), o modelo de embedding (`embeddings`) e o diretório onde a base de dados deve ser persistida (`PERSIST_DIRECTORY`). Ele gera os embeddings para cada chunk usando o modelo fornecido e os armazena na base de dados, salvando tudo no disco automaticamente.
*   `if __name__ == "__main__":`: Este bloco garante que a função `build_and_save_vector_store()` seja executada apenas quando o script for rodado diretamente (e não quando importado como um módulo em outro script).
*   (Comentários adicionais no código): Incluem opções para limpeza de arquivos temporários e a alternativa de usar `MarkdownHeaderTextSplitter`, que foi aprimorada durante a fase de refinamento da AVT.

Este script encapsula o processo de transformar conteúdo textual em uma base de conhecimento vetorial pronta para ser utilizada por um sistema de Busca Aumentada por Recuperação (RAG - Retrieval Augmented Generation), que é a base do funcionamento da Assistente Virtual.

## Seção 6: Referências e Links

*   GitHub Pages: [https://pages.github.com/](https://pages.github.com/)
*   Repositório Takwara-Tech no GitHub: [https://resck.github.io/Takwara-Tech/](https://resck.github.io/Takwara-Tech/) (URL do site publicado)
*   GitHub Docs - About branches: [https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches)
*   GitHub Docs - About pull requests: [https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
*   GitHub Docs - Diretrizes da comunidade: [https://docs.github.com/pt/site-policy/github-terms/github-community-guidelines](https://docs.github.com/pt/site-policy/github-terms/github-community-guidelines)
*   GitHub Docs - Políticas de uso aceitável: [https://docs.github.com/pt/site-policy/acceptable-use-policies/github-acceptable-use-policies](https://docs.github.com/pt/site-policy/acceptable-use-policies/github-acceptable-use-policies)
*   GitHub Docs - Termos de Serviço: [https://docs.github.com/pt/site-policy/github-terms/github-terms-of-service](https://docs.github.com/pt/site-policy/github-terms/github-terms-of-service)
*   Material for MkDocs: [https://squidfunk.github.io/mkdocs-material/](https://squidfunk.github.io/mkdocs-material/)
*   Google Cloud Functions: [https://cloud.google.com/functions](https://cloud.google.com/functions)
*   Langchain: [https://www.langchain.com/](https://www.langchain.com/)
*   Google Generative AI (Gemini/Vertex AI): [https://cloud.google.com/vertex-ai/generative](https://cloud.google.com/vertex-ai/generative)
*   ChromaDB: [https://www.trychroma.com/](https://www.trychroma.com/)
*   Web Components: [https://developer.mozilla.org/pt-BR/docs/Web/Web_Components](https://developer.mozilla.org/pt-BR/docs/Web/Web_Components)
*   Shadow DOM: [https://developer.mozilla.org/pt-BR/docs/Web/Web_Components/Using_shadow_DOM](https://developer.mozilla.org/pt-BR/docs/Web/Web_Components/Using_shadow_DOM)
*   MkDocs - Template Override: [https://www.mkdocs.org/user-guide/customizing-your-theme/#overriding-template-blocks](https://www.mkdocs.org/user-guide/customizing-your-theme/#overriding-template-blocks)
*   MarkdownHeaderTextSplitter: [https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/markdown.html](https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/markdown.html)
*   MultiQueryRetriever: [https://python.langchain.com/v0.1/docs/use_cases/question_answering/how_to/multiquery_retriever/](https://python.langchain.com/v0.1/docs/use_cases/question_answering/how_to/multiquery_retriever/)
*   Prompt Engineering: [https://www.promptingguide.ai/pt](https://www.promptingguide.ai/pt)
*   Widget Climate Clock: (Referência não específica, mas pode ser um link para o projeto global ou uma implementação específica)

---