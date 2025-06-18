// docs/assets/js/graph.js - OTIMIZADO PARA TOOLBOX E SHADOW DOM

document.addEventListener('takwara:tools-ready', (event) => {
    const shadowRoot = event.detail.shadowRoot;
    initializeKnowledgeGraph(shadowRoot);
});

function initializeKnowledgeGraph(shadowRoot) {
    console.log('Takwara Grafo: A inicializar após receber o sinal "tools-ready".');

    const container = shadowRoot.getElementById('knowledge-graph'); // Acessa via shadowRoot
    if (!container) {
        console.error('Takwara Grafo: Contêiner "knowledge-graph" não encontrado no Shadow DOM. Verifique os IDs no HTML do template da toolbox (widget-grafo.html).');
        return;
    }

    if (typeof vis === 'undefined' || typeof nodes === 'undefined' || typeof edges === 'undefined') {
        console.error('Takwara Grafo: Bibliotecas (vis-network) ou dados (nodes/edges) não carregados ou não acessíveis no escopo global. Verifique a ordem dos scripts no mkdocs.yml.');
        return;
    }

    const data = {
        nodes: new vis.DataSet(nodes),
        edges: new vis.DataSet(edges),
    };

    const options = {
        nodes: {
            shape: 'dot',
            size: 16,
            font: { size: 14, color: '#333' },
            borderWidth: 2,
        },
        edges: {
            width: 2,
            color: { inherit: 'from' },
            arrows: { to: { enabled: true, scaleFactor: 0.5 } }
        },
        physics: {
            forceAtlas2Based: {
                gravitationalConstant: -26,
                centralGravity: 0.005,
                springLength: 230,
                springConstant: 0.18,
            },
            maxVelocity: 146,
            solver: 'forceAtlas2Based',
            timestep: 0.35,
            stabilization: { iterations: 150 },
        },
        interaction: {
            navigationButtons: true,
            keyboard: true,
        },
    };

    const network = new vis.Network(container, data, options);

    network.on("selectNode", function (params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = data.nodes.get(nodeId);
            if (node.path) {
                window.location.href = `/${node.path.replace('.md', '/')}`;
            }
        }
    });
}