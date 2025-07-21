1. O que é o Google Cloud Functions? (A Teoria)
# Imagine a diferença entre uma lâmpada normal e uma lâmpada com sensor de movimento.

Servidor Tradicional (Lâmpada Normal): Você liga a lâmpada e ela fica acesa 24 horas por dia, 7 dias por semana. Mesmo que não haja ninguém na sala, ela está a consumir energia e a gastar dinheiro. Você é responsável por trocar a lâmpada se ela queimar.

Google Cloud Functions (Lâmpada com Sensor): A lâmpada está sempre desligada, sem consumir energia. Quando alguém entra na sala (um "evento" ou "gatilho"), o sensor detecta o movimento e acende a lâmpada apenas pelo tempo necessário. A pessoa sai, a lâmpada apaga-se. Você só paga pelos segundos em que a luz esteve acesa. E você nunca precisa de se preocupar em trocar a lâmpada; há um estoque infinito delas.

É exatamente assim que o Google Cloud Functions funciona. É uma plataforma "Serverless" (sem servidor).

"Serverless" não significa que não existem servidores. Eles existem, mas você não precisa de os gerir, configurar, atualizar ou proteger. O Google faz tudo isso por si.
É "Orientado a Eventos": O seu código fica "adormecido" até que um "gatilho" (trigger) o acorde. No nosso caso, o gatilho será uma requisição HTTP – ou seja, quando o nosso frontend no GitHub Pages chamar o URL da nossa API.
Escala Automaticamente: Se uma pessoa chamar a nossa API, uma "lâmpada" acende-se. Se 10.000 pessoas chamarem ao mesmo tempo, o Google acende 10.000 "lâmpadas" instantaneamente para atender a todos, sem que precisemos de fazer nada.
Por que é perfeito para nós?
Porque o nosso chatbot só precisa de "pensar" quando alguém lhe faz uma pergunta. Ele não precisa de estar a gastar recursos o tempo todo. Isso torna a nossa solução extremamente barata (o plano gratuito do Google é mais do que suficiente para começar) e infinitamente escalável.

2. Quando Faremos a Configuração? (O Timing no Nosso Plano)
A configuração e o deploy no Google Cloud são o nosso próximo grande passo, o culminar da Fase 1.

O momento exato será logo após terminarmos a preparação local. O nosso "Plano de Jogo" atualizado é:

Aguardar a instalação das dependências (pip install) terminar.
Executar o script python create_vector_store.py para gerar a pasta chroma_db.
Executar pip freeze > requirements.txt para "congelar" as versões das dependências.
NESTE MOMENTO: Com todos os nossos arquivos (main.py, requirements.txt, .env.yaml) e a pasta chroma_db prontos, iniciaremos a configuração do Google Cloud.
Portanto, é a próxima etapa assim que o seu terminal estiver livre e a base de conhecimento tiver sido criada.

3. Como Faremos a Configuração? (O Passo a Passo Prático)
Não se preocupe, eu vou guiar-te em cada detalhe quando chegar a hora. Mas, para que você já tenha uma ideia, o processo prático envolve os seguintes passos:

Criação da Conta e do Projeto: O primeiro passo será você aceder a cloud.google.com, criar uma conta gratuita (geralmente requer um cartão de crédito para verificação, mas não cobra nada dentro do plano gratuito) e criar um "Projeto" novo para o nosso chatbot.

Instalação da Ferramenta gcloud CLI: O Google oferece uma ferramenta de linha de comando (gcloud) que é a ponte entre o seu computador e a sua conta na nuvem. Vamos instalá-la e fazer login (gcloud auth login).

Ativação das APIs: Dentro do seu projeto no Google Cloud, precisamos de "ligar" as ferramentas que queremos usar. Será como ativar apps no telemóvel. Vamos ativar a "Cloud Functions API" (para permitir a criação de funções) e a "Cloud Build API" (que ajuda a "empacotar" o nosso projeto para a nuvem).

Execução do Comando de Deploy: Finalmente, com tudo preparado, executaremos um único comando no terminal, a partir da pasta backend-api, que fará toda a magia:

Bash

gcloud functions deploy chatbot-api ... (com todos os parâmetros que já vimos)
Este comando irá:

Empacotar o seu código (main.py), as dependências (requirements.txt), os segredos (.env.yaml) e a sua base de conhecimento (chroma_db).
Enviar tudo para o Google Cloud.
Configurar um servidor seguro e otimizado para rodar o seu código.
Ligar um gatilho HTTP a esse código.
E, no final, devolver-nos um URL público que será o endereço do "cérebro" do nosso chatbot.
É um passo muito emocionante e que eleva imensamente o nível técnico do projeto. Estaremos a fazer em minutos o que, há alguns anos, levaria dias ou semanas de trabalho de configuração de servidores.