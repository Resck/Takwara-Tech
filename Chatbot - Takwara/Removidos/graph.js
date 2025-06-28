// docs/assets/js/graph.js - Adaptado para Shadow DOM e evento tools-ready

// OUVINTE PRINCIPAL: Escuta pelo nosso evento customizado 'takwara:tools-ready', disparado por toolbox.js
document.addEventListener('takwara:tools-ready', (event) => {
    // Pega o shadowRoot da Tool Box que é passado no detalhe do evento
    const shadowRoot = event.detail.shadowRoot;
     // Se o shadowRoot foi recebido, chama a função de inicialização do grafo
     if (shadowRoot) {
        initializeTakwaraGraph(shadowRoot);
    } else {
        // Loga um erro se o shadowRoot não estiver disponível
        console.error('Takwara Graph: Evento "tools-ready" recebido, mas shadowRoot não encontrado no detalhe.');
    }
});

// --- FUNÇÃO DE INICIALIZAÇÃO DO GRAFO ---
// Recebe o shadowRoot da Tool Box como argumento
function initializeTakwaraGraph(shadowRoot) {
    console.log('Takwara Graph: A inicializar após receber o sinal "tools-ready".');

    // Dados do grafo - Definidos DENTRO da função para evitar erros de escopo
    const nodes = [
        { id: 1, label: "Bambu", color: '#90EE90', path: 'docs/bambu/index.md' }, // path para a página do documento
        { id: 2, label: "Tecnologia Takwara", color: '#32CD32', path: 'docs/tecnologia/index.md' },
        { id: 3, label: "Conexões Geodésicas", color: '#FFFFE0', path: 'docs/tecnologia/geodesicas.md' },
        { id: 4, label: "PU Vegetal", color: '#FFFFE0', path: 'docs/tecnologia/pu-vegetal.md' },
        { id: 5, label: "Forno Ecológico", color: '#FFFFE0', path: 'docs/tecnologia/forno-ecologico.md' },
        // Adicione mais nós aqui, definindo o 'path' para o arquivo .md correspondente
        { id: 6, label: "README", color: '#ADD8E6', path: 'docs/README.md' } // Exemplo: nó para o README
    ];
    const edges = [
        { from: 1, to: 2, label: "base da", arrows: "to" },
        { from: 2, to: 3, label: "usa", arrows: "to" },
        { from: 2, to: 4, label: "usa", arrows: "to" },
        { from: 2, to: 5, label: "usa", arrows: "to" },
        { from: 1, to: 4, label: "baseado em", arrows: "to" },
        { from: 1, to: 5, label: "inclui um", arrows: "to" },
        { from: 3, to: 1, label: "requer", arrows: "to" },
        // Adicione mais arestas aqui
         { from: 2, to: 6, label: "documentado em", arrows: "to" } // Exemplo: link da Tecnologia para o README
    ];


    // Buscar o contêiner do grafo DENTRO do Shadow DOM
    // Este elemento deve existir em partials/widget-grafo.html (que é incluído em widget-tools.html)
    const container = shadowRoot.getElementById('knowledge-graph'); // Usa shadowRoot.getElementById

    // --- VERIFICAÇÃO ESSENCIAL: O contêiner do grafo deve existir no Shadow DOM ---
    if (!container) {
        console.error('Takwara Graph: Container "#knowledge-graph" não encontrado no Shadow DOM. Verifique o HTML do template `partials/widget-grafo.html`.');
        return; // Aborta a inicialização se o contêiner não for encontrado
    }

    // Verificar se a biblioteca vis.js está disponível globalmente (mantido)
    if (typeof vis === 'undefined' || !vis.DataSet || !vis.Network) {
        console.error('Takwara Graph: A biblioteca vis.js não está carregada. Verifique se o script vis.js está incluído (mkdocs.yml).');
        return;
    }

    // Cria os DataSets para nós e arestas (mantido)
    const data = {
        nodes: new vis.DataSet(nodes),
        edges: new vis.DataSet(edges),
    };

    // Opções de visualização do grafo (mantido, com navigationButtons: false)
    const options = {
        nodes: {
            shape: 'dot',
            size: 20,
            font: { size: 14, color: '#333', face: 'Arial' },
            borderWidth: 2,
            shadow: true
        },
        edges: {
            width: 2,
            color: { inherit: 'from' },
            arrows: { to: { enabled: true, scaleFactor: 0.6 } },
            dashes: true,
            shadow: true
        },
        physics: {
             enabled: true,
             barnesHut: {
                  gravitationalConstant: -30000,
                  centralGravity: 0.5,
                  springLength: 150,
                  springConstant: 0.05,
                  damping: 0.09,
                  avoidOverlap: 0.5
             },
            solver: 'barnesHut',
            timestep: 0.5,
            stabilization: { iterations: 200, updateInterval: 25 },
        },
        interaction: {
             navigationButtons: false, // <--- DESATIVADO!
             keyboard: false,
             zoomView: true,
             dragNodes: true,
             dragView: true,
             multiselect: false,
             hover: true,
             tooltipDelay: 300,
        },
        configure: {
             enabled: false // Desativa o UI de configuração
        },
         autoResize: true, // Permite que o grafo se ajuste ao tamanho do contêiner
         height: '100%', // Configura a altura para 100% do contêiner pai (#knowledge-graph)
         width: '100%' // Configura a largura para 100% do contêiner pai
    };

    // Cria a rede vis.js no contêiner DENTRO do Shadow DOM
    const network = new vis.Network(container, data, options); // Passa o contêiner do Shadow DOM

    // Opcional: Eventos para interatividade adicional (tooltips, etc.) (mantido)


    // Adiciona funcionalidade de clique para navegar para as páginas (mantida a lógica original)
    network.on("selectNode", function (params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            // Busca o objeto nó com os dados (incluindo node.path) do DataSet
            const node = data.nodes.get(nodeId);

            // --- PASSO 1: Verificar se o nó tem um 'path' ---
            if (node.path) {
                // node.path é a string que define o caminho Markdown (ex: 'docs/tecnologia/geodesicas.md')

                // PASSO 2: Transformar 'docs/caminho/arquivo.md' no caminho relativo web '/caminho/arquivo/'
                // - Remove 'docs/' do início
                // - Remove '.md' do final
                // - Adiciona '/' no final (porque MkDocs usa URL com barra final)
                let targetPath = node.path.replace('docs/', '').replace('.md', '/');

                // PASSO 3: Tratar o caso especial do README.md ('README/') para que a URL seja a raiz ('/')
                if (targetPath === 'README/') {
                    targetPath = ''; // Caminho vazio '' representa a raiz do site MkDocs
                }

                // PASSO 4: Construir a URL COMPLETA baseada no ambiente (Local vs Publicado)
                // Detecta se está rodando localmente (mkdocs serve)
                const isLocal = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' || window.location.port === '8000';

                let finalUrl;
                if (isLocal) {
                     // AMBIENTE LOCAL: URL base é a origem + '/' + targetPath
                     finalUrl = window.location.origin + '/' + targetPath;

                } else {
                     // AMBIENTE PUBLICADO (GitHub Pages): URL base é a origem + prefixo do repositório + targetPath
                     // **AJUSTE '/Takwara-Tech/'** se o nome do seu repositório no GitHub Pages for diferente!
                     const repoBase = '/Takwara-Tech/'; // Prefixo para o nome do repositório no GitHub Pages
                     finalUrl = window.location.origin + repoBase + targetPath;
                }

                // PASSO 5: Navegar para a URL final
                console.log("Navegando para:", finalUrl); // Mostra a URL gerada no console
                window.location.href = finalUrl; // Navega o navegador para essa URL

            } else {
                // Se o nó não tem 'path' definido nos dados, não faz nada ou mostra um aviso
                console.warn(`Nó clicado (${nodeId}) não possui uma propriedade 'path'. Não é possível navegar.`);
            }
        }
    });

     console.log('Takwara Graph: Inicialização concluída.');
} // Fim da função initializeTakwaraGraph