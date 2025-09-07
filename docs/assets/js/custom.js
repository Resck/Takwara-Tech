// docs/assets/js/custom.js (Versão Final e Limpa)

// A função que inicializa todos os carrosséis que encontrar na página
function initializeSplide() {
  var splides = document.querySelectorAll('.splide');
  if (splides.length) {
    for (var i = 0; i < splides.length; i++) {
      // Verifica se o carrossel já foi inicializado para evitar erros
      if (!splides[i].classList.contains('is-initialized')) {
        new Splide(splides[i], {
          type       : 'loop',
          perPage    : 4,
          perMove    : 1,
          gap        : '0px',
          autoplay   : true,
          interval   : 3000,
          arrows     : true,
          pagination : false,
        }).mount();
      }
    }
  }
}

// O método oficial do Material for MkDocs para executar um script em cada página
if (typeof document.location$ !== 'undefined') {
  document.location$.subscribe(function() {
    // Um pequeno atraso para garantir que todo o conteúdo da página foi renderizado
    setTimeout(initializeSplide, 100); 
  });
} else {
  // Fallback para o caso de a página ser carregada sem o javascript do tema
  document.addEventListener('DOMContentLoaded', initializeSplide);
}
