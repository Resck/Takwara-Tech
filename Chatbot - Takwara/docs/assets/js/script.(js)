// =================================================================================
//              SCRIPT FINAL E FUNCIONAL (VERSÃO 6)
//      Com a detecção de clique validada, a lógica de cópia foi adicionada.
// =================================================================================

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
        const chatbotHTML = `
            <div id="chatbot-container" class="takwara-chatbot">
                <div class="chat-header"><h2>Takwara AV</h2></div>
                <div id="chat-box" class="chat-box">
                    <div class="message bot-message">Olá! Sou a assistente virtual Takwara. Como posso ajudar?</div>
                </div>
                <form id="chat-form" class="chat-form">
                    <input type="text" id="user-input" class="user-input" placeholder="Faça uma pergunta..." autocomplete="off">
                    <button type="button" id="copy-chat-button" class="copy-button" title="Copiar conversa">Copiar</button>
                    <button type="submit" class="submit-button" title="Enviar">Enviar</button>
                </form>
            </div>`;
        toolboxContent.innerHTML = chatbotHTML;
        triggerButton.addEventListener('click', () => {
            document.body.classList.toggle('toolbox-is-open');
            toolboxPanel.classList.toggle('is-open');
        });
        initializeTakwaraChatbot();
    }

    function initializeTakwaraChatbot() {
        // O "ouvinte" de clique que provou funcionar.
        document.body.addEventListener('click', function(e) {
            // Se o alvo for o botão "Copiar"...
            if (e.target.id === 'copy-chat-button') {
                
                // --- LÓGICA DE CÓPIA INSERIDA AQUI ---
                const copyButton = e.target;
                const container = copyButton.closest('#chatbot-container');
                if (!container) return; // Segurança

                const chatBox = container.querySelector('#chat-box');
                if (!chatBox) return; // Segurança

                let conversationText = "Conversa com Takwara AV\n======================\n\n";
                const messages = chatBox.querySelectorAll('.message');

                messages.forEach(message => {
                    if (message.classList.contains('bot-loading-message')) return;

                    let prefix = "";
                    if (message.classList.contains('user-message')) {
                        prefix = "Você:";
                    } else if (message.classList.contains('bot-message')) {
                        prefix = "Takwara AV:";
                    }
                    const messageContent = message.textContent;
                    conversationText += `${prefix} ${messageContent}\n\n`;
                });

                navigator.clipboard.writeText(conversationText.trim()).then(() => {
                    const originalText = copyButton.textContent;
                    copyButton.textContent = 'Copiado!';
                    copyButton.disabled = true;
                    setTimeout(() => {
                        copyButton.textContent = originalText;
                        copyButton.disabled = false;
                    }, 2000);
                }).catch(err => {
                    console.error("ERRO AO TENTAR COPIAR TEXTO:", err);
                });
                // --- FIM DA LÓGICA DE CÓPIA ---
            }
        });

        // A lógica de SUBMIT estável.
        document.body.addEventListener('submit', async function(e) {
            if (e.target.id === 'chat-form') {
                e.preventDefault();
                const chatForm = e.target;
                const container = chatForm.closest('#chatbot-container');
                if (!container) return;
                const userInput = container.querySelector('#user-input');
                const chatBox = container.querySelector('#chat-box');
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
                    if (loadingMessage) loadingMessage.remove();
                    if (!response.ok) throw new Error(`Erro de servidor: ${response.status}`);
                    const data = await response.json();
                    if (data && data.answer) {
                        addMessage(data.answer, 'bot', chatBox);
                    } else {
                        addMessage('Desculpe, a API não retornou uma resposta válida.', 'bot', chatBox);
                    }
                } catch (error) {
                    const loadingMessage = chatBox.querySelector('.bot-loading-message');
                    if (loadingMessage) loadingMessage.remove();
                    addMessage(`Desculpe, ocorreu um erro: ${error.message}`, 'bot', chatBox);
                }
            }
        });
    }

    function addMessage(text, sender, chatBox) {
        if (!chatBox) return;
        const messageElement = document.createElement('div');
        const senderClass = sender === 'bot-loading' ? 'bot-loading-message' : `${sender}-message`;
        messageElement.classList.add('message', senderClass);
        if (sender === 'bot-loading') {
            messageElement.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
        } else if (sender === 'bot' && typeof marked !== 'undefined') {
            messageElement.innerHTML = marked.parse(text);
        } else {
            messageElement.innerText = text;
        }
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupTakwaraToolbox);
    } else {
        setupTakwaraToolbox();
    }
})();