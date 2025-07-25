// docs/assets/js/custom.js

document.addEventListener('DOMContentLoaded', function() {
  initializeSplide();
});

if (typeof app !== 'undefined') {
  app.events.on('page:loaded', function() {
    initializeSplide();
  });
}

function initializeSplide() {
  var splides = document.querySelectorAll('.splide');
  
  // Objeto de opções para personalizar o carrossel
  var options = {
    type       : 'loop',      // Continua em loop
    perPage    : 4,           // MOSTRA 3 IMAGENS DE UMA VEZ
    perMove    : 1,           // MOVE 1 IMAGEM DE CADA VEZ
    gap        : '0px',      // ADICIONA UM ESPAÇO ENTRE AS IMAGENS
    autoplay   : true,        // Mantém o autoplay
    interval   : 3000,        // Intervalo de 3 segundos
    arrows     : true,        // Mantém as setas
    pagination : false,       // ESCONDE OS PONTOS, para um visual mais limpo
  };

  for ( var i = 0; i < splides.length; i++ ) {
    new Splide( splides[ i ], options ).mount();
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