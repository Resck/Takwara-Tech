document.addEventListener('DOMContentLoaded', function () {
  const openModalButton = document.getElementById('open-tools-modal');
  const closeModalButton = document.getElementById('close-tools-modal');
  const modalOverlay = document.getElementById('tools-modal');

  // Função para abrir o modal
  if (openModalButton && modalOverlay) {
    openModalButton.addEventListener('click', function () {
      modalOverlay.classList.add('active');
    });
  }

  // Função para fechar o modal
  function closeModal() {
      modalOverlay.classList.remove('active');
  }

  if (closeModalButton) {
    closeModalButton.addEventListener('click', closeModal);
  }
  
  // Fechar o modal ao clicar fora da área de conteúdo (no overlay)
  if (modalOverlay) {
      modalOverlay.addEventListener('click', function(event) {
          if (event.target === modalOverlay) {
              closeModal();
          }
      });
  }


  // Lógica para as abas dentro do modal
  const tabs = document.querySelectorAll('.takwara-tab-button');
  const panes = document.querySelectorAll('.takwara-tab-pane');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetPane = document.querySelector(tab.dataset.tabTarget);

      // Desativa todas as abas e painéis
      tabs.forEach(t => t.classList.remove('active'));
      panes.forEach(p => p.classList.remove('active'));

      // Ativa a aba clicada e o seu painel correspondente
      tab.classList.add('active');
      if (targetPane) {
        targetPane.classList.add('active');
      }
    });
  });
});