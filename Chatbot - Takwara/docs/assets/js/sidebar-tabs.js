

document.addEventListener('DOMContentLoaded', function () {
  const tabs = document.querySelectorAll('.takwara-tab-button');
  const tabPanes = document.querySelectorAll('.takwara-tab-pane');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Remove a classe 'active' de todas as abas e painéis
      tabs.forEach(t => t.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));

      // Adiciona a classe 'active' à aba e ao painel clicado
      tab.classList.add('active');
      const targetPane = document.querySelector(tab.dataset.tabTarget);
      if (targetPane) {
        targetPane.classList.add('active');
      }
    });
  });
});