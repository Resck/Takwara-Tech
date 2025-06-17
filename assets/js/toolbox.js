// docs/assets/js/toolbox.js - VERSÃO COM POLIMENTO FINAL

const TakwaraToolboxTemplate = document.createElement('template');
TakwaraToolboxTemplate.innerHTML = `
  <style>
    :host {
      position: fixed;
      left: 0;
      width: 25rem; 
      z-index: 10;

      /* 1. ANIMAÇÃO MAIS LENTA: Aumentamos a duração da transição da altura */
      transition: transform 0.3s ease-in-out, height 0.5s ease-in-out; 

      overflow-y: auto;
      background-color: var(--md-default-bg-color, #fff);
      border-right: 1px solid var(--md-typeset-hr-color, #ccc);
      top: var(--header-height);

      /* 2. AJUSTE FINO DO ENCOLHIMENTO: Subtraímos 10px extras para evitar a sobreposição */
      height: calc(100vh - var(--header-height) - var(--footer-shrink-amount) - 10px);
    }
    @media screen and (max-width: 76.25em) { :host { transform: translateX(-100%); } }
    .toolbox-inner-content { padding: 1rem; }
  </style>
  <div class="toolbox-inner-content"></div>
`;

// O resto do ficheiro (a classe, o customElements.define, etc.) continua exatamente igual...
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
      console.log('Takwara Toolbox: Evento "tools-ready" disparado.');
    document.dispatchEvent(new CustomEvent('takwara:tools-ready'));
    }
  }
}
customElements.define('takwara-toolbox', TakwaraToolbox);
document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.md-header');
    const customFooter = document.querySelector('.takwara-footer-panel');
    const headerHeight = header ? header.offsetHeight : 0;
    const toolboxElement = document.createElement('takwara-toolbox');
    toolboxElement.style.setProperty('--header-height', `${headerHeight}px`);
    toolboxElement.style.setProperty('--footer-shrink-amount', '0px');
    document.body.appendChild(toolboxElement);
    function handleScroll() {
        if (!customFooter) return;
        const footerRect = customFooter.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        if (footerRect.top < (windowHeight - (footerRect.height * 0.1))) {
            toolboxElement.style.setProperty('--footer-shrink-amount', `${customFooter.offsetHeight}px`);
        } else {
            toolboxElement.style.setProperty('--footer-shrink-amount', '0px');
        }
    }
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
});