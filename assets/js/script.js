document.addEventListener('DOMContentLoaded', () => {
    // DETETIVE 1: O script começou a ser executado?
    console.log("Script.js carregado e DOM pronto.");

    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    // DETETIVE 2: Encontramos o formulário de chat no HTML?
    console.log("Elemento do formulário:", chatForm);

    // O URL da sua API
    const apiUrl = 'https://us-central1-adroit-citadel-397215.cloudfunctions.net/chatbot-api'; 

    // Verificamos se o formulário foi encontrado antes de adicionar o "ouvinte"
    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault(); 

            // DETETIVE 3: O clique no botão "Enviar" foi detetado?
            console.log("Formulário submetido!");

            const userQuestion = userInput.value.trim();
            if (!userQuestion) return;

            addMessage(userQuestion, 'user');
            userInput.value = '';

            try {
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: userQuestion }),
                });

                if (!response.ok) { throw new Error('Erro na API'); }

                const data = await response.json();
                addMessage(data.answer, 'assistant');

            } catch (error) {
                console.error('Falha ao comunicar com a API:', error);
                addMessage('Desculpe, ocorreu um erro de comunicação.', 'assistant');
            }
        });
    } else {
        console.error("ERRO CRÍTICO: Não foi possível encontrar o elemento com id 'chat-form'. Verifique o seu HTML.");
    }

    function addMessage(text, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = text;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});