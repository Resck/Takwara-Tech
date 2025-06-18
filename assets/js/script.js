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
  
  // Acessa os elementos DENTRO do Shadow DOM
  const chatForm = shadowRoot.getElementById('chat-form');
  const chatBox = shadowRoot.getElementById('chat-box');
  const userInput = shadowRoot.getElementById('user-input');

  if (!chatForm || !chatBox || !userInput) { // Verifica todos os elementos importantes
    console.error('Takwara AVT: Um ou mais elementos HTML essenciais não foram encontrados no Shadow DOM. Verifique os IDs no HTML do template `widget-chatbot.html`.');
    return;
  }

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

      // Remove loading indicator do chatBox que está no Shadow DOM
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
    const messageElement = shadowRoot.createElement('div'); // Cria elemento no Shadow DOM
    messageElement.classList.add('message', `${sender}-message`);
    if (sender === 'bot-loading') {
      messageElement.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
    } else {
      messageElement.innerText = text;
    }
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Problema da AVT não reconhecendo textos do menu e sem referências:
  // Este é um problema de backend (API). Se ela não está citando fontes ou reconhecendo
  // o contexto, significa que a busca de similaridade ou a engenharia de prompt
  // na Google Cloud Function não está funcionando como deveria.
  // Vamos deixar para investigar isso NA PRÓXIMA FASE, após estabilizarmos o frontend.
  // Por enquanto, focamos em fazer o CHATBOT APARECER E ENVIAR MENSAGENS.
}
