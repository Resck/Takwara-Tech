document.addEventListener('DOMContentLoaded', function () {
  const mainContentArea = document.querySelector('.md-main__inner');
  if (!mainContentArea) return;

  // 1. Cria o nosso novo contentor para a barra lateral
  const toolsSidebar = document.createElement('aside');
  toolsSidebar.className = 'takwara-tools-sidebar';

  // 2. Cria o HTML para as abas e painéis
  toolsSidebar.innerHTML = `
    <nav class="takwara-sidebar-tabs">
      <button class="takwara-tab-button active" data-tab-target="#tab-toc-content">Índice</button>
      <button class="takwara-tab-button" data-tab-target="#tab-avt-content">AVT</button>
      <button class="takwara-tab-button" data-tab-target="#tab-grafo-content">Grafo</button>
    </nav>
    <div class="takwara-sidebar-content">
      <div id="tab-toc-content" class="takwara-tab-pane active"></div>
      <div id="tab-avt-content" class="takwara-tab-pane"></div>
      <div id="tab-grafo-content" class="takwara-tab-pane"></div>
    </div>
  `;

  // 3. Move os elementos originais para dentro das nossas abas
  const originalTOC = document.querySelector('.md-sidebar--secondary .md-sidebar__inner');
  const chatbotWidget = document.getElementById('chatbot-widget-container'); // Precisaremos de um container para o chatbot
  const graphWidget = document.getElementById('graph-widget-container'); // E para o grafo

  if (originalTOC) {
    toolsSidebar.querySelector('#tab-toc-content').appendChild(originalTOC);
  }
  if (chatbotWidget) {
    toolsSidebar.querySelector('#tab-avt-content').appendChild(chatbotWidget);
  }
  if (graphWidget) {
    toolsSidebar.querySelector('#tab-grafo-content').appendChild(graphWidget);
  }

  // 4. Adiciona a nossa nova barra lateral à página
  mainContentArea.appendChild(toolsSidebar);

  // 5. Adiciona a lógica para as abas funcionarem
  const tabs = toolsSidebar.querySelectorAll('.takwara-tab-button');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const target = document.querySelector(tab.dataset.tabTarget);
      toolsSidebar.querySelectorAll('.takwara-tab-pane').forEach(p => p.classList.remove('active'));
      if(target) target.classList.add('active');
    });
  });
});