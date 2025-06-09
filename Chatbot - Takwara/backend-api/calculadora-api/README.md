Guia de Incorporação: Calculadora de Domos Geodésicos
Este documento detalha a arquitetura e o funcionamento da calculadora de domos geodésicos interativa integrada ao site da Tecnologia Takwara.

1. Visão Geral da Arquitetura
A calculadora foi construída com uma arquitetura moderna que separa a lógica de cálculo da interface do utilizador. Isto é conhecido como uma arquitetura de "frontend" e "backend" desacoplados.

O Backend (O "Cérebro" de Cálculo):

É uma API Serverless construída com Python e o micro-framework Flask.
Está publicada na nuvem através do Google Cloud Functions.
A sua única responsabilidade é receber dados (diâmetro, frequência, truncagem), executar a lógica matemática e devolver os resultados em formato de dados puros (JSON).
Todo o código-fonte do backend reside na pasta calculadora-api/.
O Frontend (O "Rosto" da Calculadora):

É um "widget" flutuante criado com HTML, CSS e JavaScript.
Ele não é uma página fixa, mas sim um componente que é injetado dinamicamente em todas as páginas do site.
A sua responsabilidade é apresentar um formulário ao utilizador, enviar os dados para a API do backend, receber a resposta e exibir os resultados de forma amigável.
O código que controla este widget reside no arquivo docs/assets/js/calculadora.js.
2. Como Funciona: O Fluxo de Dados
O processo completo, desde a interação do utilizador até à exibição do resultado, segue estes passos:

Um utilizador visita qualquer página do site (resck.github.io/Takwara-Tech).
O arquivo calculadora.js é carregado junto com a página.
O script cria o HTML do widget da calculadora e o injeta no canto inferior direito da tela.
O utilizador insere os dados (ex: diâmetro 10, frequência 3) e clica no botão "Calcular".
O JavaScript interceta este clique, empacota os dados num objeto JSON e envia uma requisição POST para o URL da nossa API na nuvem.
A API no Google Cloud "acorda", recebe os dados, executa a lógica de cálculo em Python que está no main.py e calcula os comprimentos e quantidades das peças.
A API devolve uma resposta JSON com os resultados (ex: {"success": true, "segment_lengths": {...}}).
O JavaScript no navegador recebe esta resposta, constrói dinamicamente uma tabela HTML com os dados e insere-a na área de "Resultados" do widget.
3. Como Modificar e Manter
Para Modificar a Aparência do Widget:
Toda a aparência do formulário, da tabela e do posicionamento do widget é controlada pelo bloco de CSS que está dentro do arquivo docs/assets/js/calculadora.js. Procure pela variável const calculatorCSS = \...`;` e edite as regras de estilo conforme necessário.
Para Modificar a Lógica de Cálculo:
Esta é a modificação mais importante.
Abra o arquivo calculadora-api/main.py.
Encontre a secção comentada --- A sua lógica de cálculo ---.
Substitua a lógica de exemplo pelas suas fórmulas matemáticas precisas para cada frequência e tipo de truncagem.
Importante: Após alterar o main.py, você precisa de fazer um novo deploy da API para que as alterações fiquem online. Use o comando:
Bash

# Estando dentro da pasta 'calculadora-api'
gcloud functions deploy calculadora-domo-api ... (com todos os parâmetros)
Para Adicionar ou Mudar as Imagens dos Domos:
Faça o upload das suas imagens para a pasta docs/assets/images/.
Abra o arquivo docs/assets/js/calculadora.js.
Encontre o objeto const domeImages = {...};.
Substitua os URLs de placeholder pelos caminhos relativos para as suas imagens. Exemplo:
JavaScript

const domeImages = {
    1: 'assets/images/domo-1v.png',
    2: 'assets/images/domo-2v.png',
    // ... e assim por diante
};
4. Fluxo de Publicação de Alterações
Para que qualquer alteração no frontend (visual ou de interatividade) apareça no seu site público:

Teste Localmente: Use o comando mkdocs serve na pasta raiz (Chatbot - Takwara) para ver as suas alterações em tempo real no endereço http://127.0.0.1:8000.
Salve no GitHub: Use o fluxo git add ., git commit -m "Sua mensagem" e git push para salvar o código-fonte das suas alterações.
Publique o Site: Execute mkdocs gh-deploy na pasta raiz para publicar a nova versão do site para o mundo.
