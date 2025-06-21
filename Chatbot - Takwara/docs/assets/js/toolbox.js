// docs/assets/js/toolbox.js - VERSÃO FINAL COM LAYOUT CORRIGIDO E AJUSTES DE FONTE

const TakwaraToolboxTemplate = document.createElement('template');
TakwaraToolboxTemplate.innerHTML = `
  <style>
    /* Estilos básicos do host para posicionamento */
    :host {
      position: fixed;
      left: 0;
      width: 25rem; /* Largura da Tool Box */
      z-index: 10; /* Garante que fica acima de outros elementos */
      /* Transição para suavizar a mudança de altura */
      transition: transform 0.3s ease-in-out, height 0.5s ease-in-out;

      overflow-y: auto; /* Adiciona scroll se o conteúdo for maior que a altura */
      background-color: var(--md-default-bg-color, #fff); /* Cor de fundo */
      border-right: 1px solid var(--md-typeset-hr-color, #ccc); /* Borda à direita */
      top: var(--header-height); /* Posição inicial abaixo do cabeçalho */

      /* Altura dinâmica: tela cheia menos cabeçalho, rodapé (quando visível) e uma pequena margem */
      height: calc(100vh - var(--header-height) - var(--footer-shrink-amount) - 10px);
      padding-bottom: 10px; /* Adiciona um padding no final para o scroll */
    }

    /* Media query para telas menores: esconde a Tool Box por padrão */
    @media screen and (max-width: 76.25em) {
        :host {
            transform: translateX(-100%); /* Move para fora da tela */
        }
        /* Opcional: Adicionar uma forma de ativá-la em mobile (ex: botão no header que mude o transform) */
    }

    /* Estilo para o contêiner interno do conteúdo das ferramentas (flexbox) */
    .toolbox-inner-content {
      padding: 1rem;
      display: flex;          /* Usa flexbox */
      flex-direction: column; /* Empilha os elementos filhos (tool-section) verticalmente */
      gap: 1.5rem;            /* Adiciona espaço entre os elementos empilhados */
      width: 100%;            /* Garante que o contêiner interno usa toda a largura */
      box-sizing: border-box; /* Inclui padding na largura */
    }

    /* Estilo para cada seção de ferramenta (AVT, Grafo, Calculadora) */
    .tool-section {
        width: 100%; /* Garante que cada seção ocupe a largura total disponível */
        /* Opcional: Separador visual entre as seções */
        border-bottom: 1px solid var(--md-typeset-hr-color, #eee);
        padding-bottom: 1.5rem; /* Espaço abaixo do separador */
         margin-bottom: 0 !important; /* Garante que não há margem inferior extra */
    }

    /* Remove a borda inferior da última seção para não ter um separador no final */
    .tool-section:last-child {
        border-bottom: none;
        padding-bottom: 0;
         margin-bottom: 0 !important;
    }

    /* --- AJUSTES DE FONTE E TAMANHO --- */

    /* Estilo para os títulos H4 dentro das seções da Tool Box (Ex: "Converse com Takwara") */
    .tool-section h4 {
        font-size: 1rem; /* Tamanho do título H4 - Ajustado para ser menor que o texto da AVT */
        margin-top: 0;
        margin-bottom: 0.5rem; /* Espaço abaixo do título */
        color: var(--md-default-fg-color, rgba(0, 0, 0, 0.87));
    }

    /* Estilo para o texto introdutório P nas seções da Tool Box (Ex: "Tire as suas dúvidas...") */
    .tool-section p {
         font-size: 0.85rem; /* Tamanho do texto P - Ajustado */
         margin-top: 0;
         margin-bottom: 1rem; /* Espaço abaixo da descrição e antes do conteúdo da ferramenta */
         color: var(--md-default-fg-color, rgba(0, 0, 0, 0.6));
    }

    /* Estilo para todas as mensagens no chatbox */
    .chat-box .message {
        font-size: 1rem; /* Tamanho do texto da mensagem da AVT - Ajustado para ser maior que o título H4 */
        margin-bottom: 0.8rem;
        line-height: 1.5;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        max-width: 90%;
        word-wrap: break-word;
    }

    /* Estilos específicos para mensagens do usuário e bot (mantidos) */
    .user-message { /* ... */ }
    .bot-message { /* ... */ }

    /* Ajustes para o contêiner das mensagens (mantido) */
    .chat-box {
         height: 300px; /* Mantenha uma altura fixa para scroll */
         overflow-y: auto;
         display: flex;
         flex-direction: column;
         padding: 0.5rem;
         border: 1px solid var(--md-typeset-table-color, #ccc); /* Borda */
         border-radius: 8px;
         margin-bottom: 1rem;
    }

    /* Estilo para o indicador de digitação (mantido) */
    .bot-loading .typing-indicator { /* ... */ }

    /* Estilo para o botão Copiar Conversa (se o estilo não estiver no HTML) */
     #copy-chat-button {
         margin-top: 0.5rem;
         padding: 5px 10px;
         background-color: #007bff;
         color: white;
         border: none;
         border-radius: 4px;
         cursor: pointer;
         font-size: 0.9rem;
     }

    /* Ajustes para o contêiner do grafo (essencial para o vis.js) */
    .knowledge-graph-canvas {
         width: 100% !important;
         height: 400px; /* Mantenha uma altura para a visualização */
    }

    /* CSS para esconder a instrumentação padrão do vis.js */
    .vis-network-manipulation { display: none !important; }
    .vis-navigation { display: none !important; }
    .vis-overlay { display: none !important; }


  </style>
  <div class="toolbox-inner-content"></div>
`;

class TakwaraToolbox extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.appendChild(TakwaraToolboxTemplate.content.cloneNode(true));
  }

  connectedCallback() {
    const toolsContainer = this.shadowRoot.querySelector('.toolbox-inner-content');
    const globalTemplate = document.getElementById('takwara-tools-template');

    if (globalTemplate) {
      const toolsContent = globalTemplate.content.cloneNode(true);
      toolsContainer.appendChild(toolsContent);
      console.log('Takwara Toolbox: Conteúdo do template anexado ao Shadow DOM.');

      setTimeout(() => {
           const event = new CustomEvent('takwara:tools-ready', {
               bubbles: true, composed: true,
               detail: { shadowRoot: this.shadowRoot }
           });
           document.dispatchEvent(event);
           console.log('Takwara Toolbox: Evento "tools-ready" disparado.');
      }, 0);

    } else {
        console.error('Takwara Toolbox: Template "takwara-tools-template" não encontrado.');
    }
  }
}
customElements.define('takwara-toolbox', TakwaraToolbox);

document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.md-header');
    const customFooter = document.querySelector('.takwara-footer-panel');
    const headerHeight = header ? header.offsetHeight : 0;

    if (!document.querySelector('takwara-toolbox')) {
         const toolboxElement = document.createElement('takwara-toolbox');
         toolboxElement.style.setProperty('--header-height', `${headerHeight}px`);
         toolboxElement.style.setProperty('--footer-shrink-amount', '0px');
         document.body.appendChild(toolboxElement);
         console.log('Takwara Toolbox: Elemento customizado <takwara-toolbox> adicionado ao DOM.');

         function handleScroll() {
             const currentCustomFooter = document.querySelector('.takwara-footer-panel');
             if (!currentCustomFooter) {
                 toolboxElement.style.setProperty('--footer-shrink-amount', '0px');
                 return;
             }
             const footerRect = currentCustomFooter.getBoundingClientRect();
             const windowHeight = window.innerHeight;
             if (footerRect.top < (windowHeight - (footerRect.height * 0.1))) {
                  toolboxElement.style.setProperty('--footer-shrink-amount', `${currentCustomFooter.offsetHeight}px`);
             } else {
                  toolboxElement.style.setProperty('--footer-shrink-amount', '0px');
             }
         }
         window.addEventListener('scroll', handleScroll, { passive: true });
         handleScroll();
    } else {
        console.warn('Takwara Toolbox: Elemento customizado <takwara-toolbox> já existe no DOM.');
    }
});