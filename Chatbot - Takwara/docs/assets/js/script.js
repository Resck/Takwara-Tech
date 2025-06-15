// Usamos esta variável global para garantir que o script só é inicializado uma vez.
if (window.takwaraScriptLoaded === undefined) {
    window.takwaraScriptLoaded = true;
    
    // URL da tua API na nuvem.
   // const API_URL = 'https://southamerica-east1-adroit-citadel-397215.cloudfunctions.net/chatbot-api';
   const API_URL = 'https://southamerica-east1-adroit-citadel-397215.cloudfunctions.net/chatbot-api';

    // Espera que todo o conteúdo da página seja carregado antes de executar o código.
    document.addEventListener('DOMContentLoaded', () => {
        console.log('Script.js executado.');
        const chatForm = document.getElementById('chat-form');
        
        if (chatForm) {
            console.log('Formulário de chat encontrado. A inicializar...');
            const chatBox = document.getElementById('chat-box');
            const userInput = document.getElementById('user-input');

            // Adiciona um "ouvinte" para quando o formulário for submetido (botão Enviar clicado).
            chatForm.addEventListener('submit', async (e) => {
                e.preventDefault(); // Impede que a página recarregue.
                const userMessage = userInput.value.trim();
                if (!userMessage) return; // Não faz nada se a mensagem estiver vazia.

                addMessage(userMessage, 'user');
                userInput.value = ''; // Limpa o campo de texto.

                // Este é o bloco completo e corrigido para fazer a chamada à API.
                try {
                    addMessage('...', 'bot-loading');
                    
                    // Técnica de cache-busting para garantir que o pedido é sempre novo.
                    const cacheBustingURL = `${API_URL}?t=${new Date().getTime()}`;
                    console.log('A contactar o URL com cache-busting:', cacheBustingURL);

                    const pageContext = window.location.pathname;
console.log("Contexto da página enviado:", pageContext);

const response = await fetch(cacheBustingURL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    // Adicionamos o contexto ao corpo do pedido
    body: JSON.stringify({ 
      query: userMessage,
      context: pageContext 
    })
});

                    const loadingMessage = chatBox.querySelector('.bot-loading');
                    if (loadingMessage) {
                        chatBox.removeChild(loadingMessage);
                    }

                    if (!response.ok) {
                        throw new Error(`Erro de comunicação com o servidor: ${response.status} ${response.statusText}`);
                    }

                    const data = await response.json();
                    console.log('Dados recebidos:', data);
                    
                    if (data.answer) {
                        addMessage(data.answer, 'bot');
                    } else {
                        addMessage('A API respondeu, mas sem uma resposta válida.', 'bot');
                    }

                } catch (error) {
                    console.error('Ocorreu um erro DURANTE o fetch:', error);
                    
                    const loadingMessage = chatBox.querySelector('.bot-loading');
                    if (loadingMessage) {
                        chatBox.removeChild(loadingMessage);
                    }
                    
                    addMessage('Desculpe, ocorreu um erro de comunicação. Por favor, tente novamente.', 'bot');
                }
            });

            // Função auxiliar para adicionar mensagens à caixa de chat.
            function addMessage(text, sender) {
                const messageElement = document.createElement('div');
                messageElement.classList.add('message', `${sender}-message`);
                
                if (sender === 'bot-loading') {
                    messageElement.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
                } else {
                    messageElement.textContent = text;
                }
                
                chatBox.appendChild(messageElement);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

        } else {
            console.log('Formulário de chat não encontrado nesta página.');
        }
    });
}