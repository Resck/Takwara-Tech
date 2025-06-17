// docs/assets/js/script.js - Versão que "escuta" o evento certo

function initializeTakwaraChatbot() {
  console.log('Takwara AVT: A inicializar após receber o sinal "tools-ready".');

  const API_URL = 'https://southamerica-east1-adroit-citadel-397215.cloudfunctions.net/chatbot-api';
  const chatForm = document.getElementById('chat-form');

  if (!chatForm) {
    console.error('Takwara AVT: Formulário de chat não encontrado. Verifique os IDs no HTML.');
    return;
  }

  const chatBox = document.getElementById('chat-box');
  const userInput = document.getElementById('user-input');

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
      addMessage(data.answer || 'Não obtive uma resposta válida.', 'bot');

    } catch (error) {
      console.error('Takwara AVT: Erro durante a chamada à API:', error);
      chatBox.querySelector('.bot-loading')?.remove();
      addMessage('Desculpe, ocorreu um erro de comunicação. Tente novamente.', 'bot');
    }
  });

  function addMessage(text, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    if (sender === 'bot-loading') {
      messageElement.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
    } else {
      messageElement.innerText = text;
    }
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
}

// OUVINTE PRINCIPAL: Escuta pelo nosso evento customizado.
document.addEventListener('takwara:tools-ready', initializeTakwaraChatbot);