// Espera que a página inteira esteja carregada para começar a trabalhar.
document.addEventListener('DOMContentLoaded', function () {

  // O 'md-grid' é o container principal que segura todo o conteúdo da página no tema.
  const mainGridContainer = document.querySelector('.md-grid');

  // Só executa o código se encontrar este container.
  if (mainGridContainer) {

    // 1. CRIA A COLUNA DA ESQUERDA
    const leftColumn = document.createElement('aside');
    leftColumn.className = 'takwara-left-column';
    leftColumn.innerHTML = `
      <h3>Navegação Global</h3>
      <p>(Índice principal do site)</p>
      <hr>
      <h4>O Bambu Vem Primeiro!</h4>
      <p>(Calls to action)</p>
    `;

    // 2. CRIA A COLUNA DA DIREITA
    const rightColumn = document.createElement('aside');
    rightColumn.className = 'takwara-right-column';
    rightColumn.innerHTML = `<h3>Nesta Página</h3>`;

    // 3. ENCONTRA O ÍNDICE ORIGINAL DA PÁGINA
    const originalToc = document.querySelector('.md-sidebar--secondary');
    if (originalToc) {
      // Se o índice existir, move-o para dentro da nossa nova coluna direita.
      rightColumn.appendChild(originalToc);
    }

    // 4. MONTA O NOVO LAYOUT
    // Insere a nossa nova coluna esquerda no início do container principal.
    mainGridContainer.prepend(leftColumn);

    // Adiciona a nossa nova coluna direita no final do container principal.
    mainGridContainer.appendChild(rightColumn);
  }
});