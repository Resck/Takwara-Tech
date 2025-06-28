// O CÓDIGO DE OURO - VERSÃO FINAL COM MELHORIAS DE LAYOUT

(function() {
    function setupTakwaraToolbox() {
        if (document.querySelector('.takwara-push-sidebar')) return;
        const toolboxPanel = document.createElement('div');
        toolboxPanel.className = 'takwara-push-sidebar';
        const toolboxContent = document.createElement('div');
        toolboxContent.className = 'takwara-toolbox-content';
        toolboxPanel.appendChild(toolboxContent);
        document.body.appendChild(toolboxPanel);
        const triggerButton = document.createElement('button');
        triggerButton.textContent = 'Takwara AV';
        triggerButton.className = 'takwara-toolbox-trigger';
        document.body.appendChild(triggerButton);
        const chatbotHTML = `<div id="chatbot-container" class="takwara-chatbot"><div id="chat-box" class="chat-box"><div class="message bot-message">Olá! Sou a assistente virtual Takwara. Como posso ajudar?</div></div><form id="chat-form" class="chat-form"><input type="text" id="user-input" class="user-input" placeholder="Faça uma pergunta..." autocomplete="off"><button type="submit" class="submit-button" title="Enviar">Enviar</button></form></div>`;
        toolboxContent.innerHTML = chatbotHTML;
        triggerButton.addEventListener('click', () => {
            document.body.classList.toggle('toolbox-is-open');
            toolboxPanel.classList.toggle('is-open');
        });
        initializeTakwaraChatbot();
    }

    function initializeTakwaraChatbot() {
        document.body.addEventListener('submit', async function(e) {
            if (e.target && e.target.id === 'chat-form') {
                e.preventDefault();
                const chatForm = e.target;
                const chatbotContainer = chatForm.closest('.takwara-chatbot');
                if (!chatbotContainer) return;
                const userInput = chatbotContainer.querySelector('#user-input');
                const chatBox = chatbotContainer.querySelector('#chat-box');
                if (!userInput || !chatBox) return;
                const userMessage = userInput.value.trim();
                if (!userMessage) return;
                addMessage(userMessage, 'user', chatBox);
                userInput.value = '';
                const API_URL = 'https://southamerica-east1-adroit-citadel-397215.cloudfunctions.net/chatbot-api';
                try {
                    addMessage('...', 'bot-loading', chatBox);
                    const response = await fetch(API_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query: userMessage, context: window.location.pathname })
                    });
                    const loadingMessage = chatBox.querySelector('.bot-loading-message');
                    if(loadingMessage) loadingMessage.remove();
                    if (!response.ok) throw new Error(`Erro de servidor: ${response.status}`);
                    const data = await response.json();
                    if (data && data.answer) {
                        addMessage(data.answer, 'bot', chatBox);
                    } else {
                        addMessage('Desculpe, a API não retornou uma resposta válida.', 'bot', chatBox);
                    }
                } catch (error) {
                    const loadingMessage = chatBox.querySelector('.bot-loading-message');
                    if(loadingMessage) loadingMessage.remove();
                    addMessage(`Desculpe, ocorreu um erro de comunicação: ${error.message}`, 'bot', chatBox);
                }
            }
        });
    }

    // ================== MELHORIA NA FUNÇÃO addMessage ==================
    /**
     * Função para adicionar mensagens. Agora ela verifica se a biblioteca 'marked' existe.
     * Se existir e a mensagem for do 'bot', ela converte o Markdown para HTML.
     */
    function addMessage(text, sender, chatBox) {
        if (!chatBox) return;
        const messageElement = document.createElement('div');
        const senderClass = sender === 'bot-loading' ? 'bot-loading-message' : `${sender}-message`;
        messageElement.classList.add('message', senderClass);

        if (sender === 'bot-loading') {
            messageElement.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
        } else if (sender === 'bot' && typeof marked !== 'undefined') {
            // Se a mensagem for do bot e a biblioteca 'marked' estiver carregada, use-a!
            messageElement.innerHTML = marked.parse(text);
        } else {
            // Para mensagens do usuário, usamos innerText para segurança.
            messageElement.innerText = text;
        }
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    // ====================================================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupTakwaraToolbox);
    } else {
        setupTakwaraToolbox();
    }
})();