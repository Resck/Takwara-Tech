// docs/assets/js/script.js - Versão que "escuta" o evento certo e usa shadowRoot

// OUVINTE PRINCIPAL: Escuta pelo nosso evento customizado.
document.addEventListener('takwara:tools-ready', (event) => {
    // Pega o shadowRoot do detalhe do evento
    const shadowRoot = event.detail.shadowRoot;
    initializeTakwaraChatbot(shadowRoot);
});

function initializeTakwaraChatbot(shadowRoot) {
  console.log('Takwara AVT: A inicializar após receber o sinal "tools-ready".');

  const API_URL = 'https://southamerica-east1-adroit-citadel-397215.cloudfunctions.net/chatbot-api';

  // --- ACESSA OS ELEMENTOS DENTRO DO Shadow DOM ---
  // Garanta que estas declarações estão presentes e são únicas
  const chatForm = shadowRoot.getElementById('chat-form');
  const chatBox = shadowRoot.getElementById('chat-box');
  const userInput = shadowRoot.getElementById('user-input');
  const copyChatButton = shadowRoot.getElementById('copy-chat-button'); // <-- DECLARAÇÃO CORRETA AQUI


  // --- Verificar se todos os elementos HTML essenciais foram encontrados ---
  // Inclua copyChatButton na verificação
  if (!chatForm || !chatBox || !userInput || !copyChatButton) {
    console.error('Takwara AVT: Um ou mais elementos HTML essenciais não foram encontrados no Shadow DOM. Verifique os IDs em `partials/widget-chatbot.html`.');
    // Opcional: logar quais elementos faltam para depuração
    // console.log("Elementos não encontrados:", { chatForm, chatBox, userInput, copyChatButton });
    return; // Aborta a inicialização
  }

  // --- Lógica para o Formulário de Chat ---
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userMessage = userInput.value.trim();
    if (!userMessage) return;

    addMessage(userMessage, 'user');
    userInput.value = '';

    try {
      addMessage('...', 'bot-loading');
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage, context: window.location.pathname })
      });

      chatBox.querySelector('.bot-loading')?.remove();
      if (!response.ok) throw new Error(`Erro de servidor: ${response.status}`);

      const data = await response.json();
      // Verifica se a resposta da API inclui a chave 'answer'
      if (data && data.answer) {
          addMessage(data.answer, 'bot');
      } else {
          // Se a API não retornou 'answer', mas não deu erro HTTP, pode ser um problema no backend
          console.error("Takwara AVT: Resposta da API recebida, mas sem a chave 'answer'.", data);
          addMessage('Desculpe, não consegui processar a resposta da API.', 'bot');
      }


    } catch (error) {
      console.error('Takwara AVT: Erro durante a chamada à API:', error);
      chatBox.querySelector('.bot-loading')?.remove();
      addMessage('Desculpe, ocorreu um erro de comunicação. Tente novamente.', 'bot');
    }
  });

  // --- Lógica para o Botão Copiar Conversa ---
  // O listener AGORA está no escopo correto
  copyChatButton.addEventListener('click', () => {
      let conversationText = "Conversa com Takwara AVT:\n\n"; // Título para a conversa copiada

      // Seleciona todas as mensagens no chatbox dentro do Shadow DOM
      const messages = chatBox.querySelectorAll('.message');

      messages.forEach(messageElement => {
          const senderClass = messageElement.classList.contains('user-message') ? 'User' : 'Takwara AVT';
          // Para mensagens do bot renderizadas com Markdown, innerText pode não pegar a formatação
          // Se a mensagem original estiver em innerHTML (do Markdown), tentamos pegar innerText primeiro
          // OU, se marked.js foi usado, pegamos innerHTML
          const messageContent = messageElement.innerHTML.includes('<p>') ? messageElement.innerHTML : messageElement.innerText || messageElement.textContent; // Tenta pegar HTML (Markdown) ou texto simples

          // Ignora o indicador de loading na cópia
          if (!messageElement.classList.contains('bot-loading')) {
               // Remove tags HTML da cópia para texto puro
               const plainTextContent = messageContent.replace(/<[^>]*>/g, ''); // Remove tags HTML
               conversationText += `${senderClass}: ${plainTextContent}\n`;
          }
      });

      // Copia o texto formatado para a área de transferência
      navigator.clipboard.writeText(conversationText)
          .then(() => {
              console.log('Conversa copiada para a área de transferência.');
              const originalText = copyChatButton.textContent;
              copyChatButton.textContent = 'Copiado!';
              setTimeout(() => {
                  copyChatButton.textContent = originalText;
              }, 2000);
          })
          .catch(err => {
              console.error('Erro ao copiar conversa: ', err);
              const originalText = copyChatButton.textContent;
               copyChatButton.textContent = 'Erro!';
               setTimeout(() => {
                   copyChatButton.textContent = originalText;
               }, 2000);
          });
  });
  // --- FIM da Lógica do Botão Copiar ---


  // --- Função addMessage (Completa, lida com Markdown e Scroll) ---
  // Esta função deve estar dentro de initializeTakwaraChatbot para acessar chatBox
  function addMessage(text, sender) {
      const messageElement = document.createElement('div'); // Cria elemento no Shadow DOM
      messageElement.classList.add('message', `${sender}-message`);

      // --- Ajuste de Tamanho de Texto via CSS (Toolbox.js) ---
      // O tamanho do texto será controlado pelo CSS na tag <style> em toolbox.js
      // Adicionaremos uma regra lá para .message { font-size: ...; }

      if (sender === 'bot-loading') {
          // Indicador de carregamento (mantido)
          messageElement.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
      } else if (sender === 'bot') {
          // --- Habilitar Markdown para mensagens do bot ---
          // Verificar se marked está carregado (deve estar via mkdocs.yml)
          if (typeof marked !== 'undefined') {
              // Usa marked.parse() para converter texto Markdown em HTML
              // marked.parse pode retornar tags <p>, então o CSS para .message P {...} pode ser necessário
              messageElement.innerHTML = marked.parse(text);
          } else {
              // Fallback se marked não estiver carregado
              messageElement.innerText = text;
              console.error("Marked.js não carregado. Não é possível renderizar Markdown.");
          }
      } else { // sender === 'user'
          // Para mensagens do usuário, usamos innerText para evitar injeção de HTML (segurança)
          messageElement.innerText = text;
      }

      chatBox.appendChild(messageElement);
      // Rola para a última mensagem
      chatBox.scrollTop = chatBox.scrollHeight;
  }
  // --- FIM da função addMessage ---


  console.log('Takwara AVT: Inicialização concluída.');
} // Fim de initializeTakwaraChatbot

// --- FIM da função addMessage ---

  // Problema da AVT não reconhecendo textos do menu e sem referências:
  // Este é um problema de backend (API). Se ela não está citando fontes ou reconhecendo
  // o contexto, significa que a busca de similaridade ou a engenharia de prompt
  // na Google Cloud Function não está funcionando como deveria.
  // Vamos deixar para investigar isso NA PRÓXIMA FASE, após estabilizarmos o frontend.
  // Por enquanto, focamos em fazer o CHATBOT APARECER E ENVIAR MENSAGENS.

