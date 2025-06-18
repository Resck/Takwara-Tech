// docs/assets/js/graph.js
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('knowledge-graph');
    if (!container) return; // Só executa se encontrar a "tela" do grafo

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

    // Adiciona funcionalidade de clique para navegar para as páginas
    network.on("selectNode", function (params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = data.nodes.get(nodeId);
            if (node.path) {
                // Navega para o caminho relativo ao site
                window.location.href = `../${node.path.replace('.md', '/')}`;
            }
        }
    });
});