// docs/assets/js/calculadora.js - VERSÃO FINAL COMPLETA COM IMAGENS E MODAL

document.addEventListener('DOMContentLoaded', () => {
    // A base de dados que o seu backend usa para popular os menus dinamicamente.
    // ATUALIZADO: 'truncation' agora é consistentemente um objeto para todas as frequências.
    // O 'total_vertices' ainda pode ser um objeto para frequências com múltiplas truncagens.
    const DOME_DATA = {
        "Icosahedron": {
            "V1": {"truncation": {"2/3": true}, "total_vertices": 11},
            "V2": {"truncation": {"1/2": true}, "total_vertices": 26},
            "V3": {"truncation": {"3/8": true, "5/8": true}, "total_vertices": {"3/8": 46, "5/8": 61}},
            "V4": {"truncation": {"1/2": true}, "total_vertices": 91},
            "L3": {"truncation": {"1/2": true}, "total_vertices": 91},
            "V5": {"truncation": {"7/15": true, "8/15": true}, "total_vertices": {"7/15": 126, "8/15": 151}},
            "V6": {"truncation": {"1/2": true}, "total_vertices": 196},
            "2V.3V": {"truncation": {"1/2": true}, "total_vertices": 196}
        },
        "Cube": {
            "V1": {"truncation": {"N/D": true}, "total_vertices": "N/D"},
            "V2": {"truncation": {"N/D": true}, "total_vertices": "N/D"},
            "V3": {"truncation": {"N/D": true}, "total_vertices": "N/D"},
            "V4": {"truncation": {"N/D": true}, "total_vertices": "N/D"},
            "V5": {"truncation": {"~1/2": true}, "total_vertices": 166},
            "V6": {"truncation": {"1/2": true}, "total_vertices": 235},
            "2V.3V": {"truncation": {"1/2": true}, "total_vertices": 235},
            "3V.2V": {"truncation": {"1/2": true}, "total_vertices": 235}
        },
        "Octahedron": {
            "V1": {"truncation": {"1/2": true}, "total_vertices": 5},
            "V2": {"truncation": {"1/2": true}, "total_vertices": 13},
            "V3": {"truncation": {"1/2": true}, "total_vertices": 25},
            "L3_3/8": {"truncation": {"3/8": true}, "total_vertices": "N/D"},
            "L3_5/8": {"truncation": {"5/8": true}, "total_vertices": "N/D"},
            "V4": {"truncation": {"N/D": true}, "total_vertices": "N/D"},
            "V5": {"truncation": {"N/D": true}, "total_vertices": "N/D"},
            "V6": {"truncation": {"N/D": true}, "total_vertices": "N/D"}
        },
        "Dodecahedron": {
            "L1": {"truncation": {"N/D": true}, "total_vertices": 32},
            "L2": {"truncation": {"N/D": true}, "total_vertices": "N/D"},
            "L2T": {"truncation": {"N/D": true}, "total_vertices": "N/D"}
        },
        "Tetrahedron": {
            "L2T": {"truncation": {"N/D": true}, "total_vertices": 10},
            "L3T": {"truncation": {"N/D": true}, "total_vertices": "N/D"}
        }
    };

    // Nova base de dados para URLs de imagens de diagramas
    // Use "uploaded:image_53a331.png-3bd87591-3b88-43d9-99ea-14781c806ce2" para a imagem fornecida pelo usuário.
    // Para outros, use placeholders que você pode substituir por suas próprias imagens.
    const DOME_IMAGES = {
        "Icosahedron": {
            "V1": { "2/3": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+V1+2%2F3" },
            "V2": { "1/2": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+V2+1%2F2" },
            "V3": {
                "3/8": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+V3+3%2F8",
                "5/8": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+V3+5%2F8"
            },
            "V4": { "1/2": "uploaded:image_53a331.png-3bd87591-3b88-43d9-99ea-14781c806ce2" }, // Imagem fornecida pelo usuário
            "L3": { "1/2": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+L3+1%2F2" },
            "V5": {
                "7/15": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+V5+7%2F15",
                "8/15": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+V5+8%2F15"
            },
            "V6": { "1/2": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+V6+1%2F2" },
            "2V.3V": { "1/2": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+2V.3V+1%2F2" }
        },
        "Cube": {
            "V1": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Cubo+V1" },
            "V2": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Cubo+V2" },
            "V3": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Cubo+V3" },
            "V4": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Cubo+V4" },
            "V5": { "~1/2": "https://placehold.co/600x400/cccccc/000000?text=Cubo+V5+~1%2F2" },
            "V6": { "1/2": "https://placehold.co/600x400/cccccc/000000?text=Cubo+V6+1%2F2" },
            "2V.3V": { "1/2": "https://placehold.co/600x400/cccccc/000000?text=Cubo+2V.3V+1%2F2" },
            "3V.2V": { "1/2": "https://placehold.co/600x400/cccccc/000000?text=Cubo+3V.2V+1%2F2" }
        },
        "Octahedron": {
            "V1": { "1/2": "https://placehold.co/600x400/cccccc/000000?text=Octaedro+V1+1%2F2" },
            "V2": { "1/2": "https://placehold.co/600x400/cccccc/000000?text=Octaedro+V2+1%2F2" },
            "V3": { "1/2": "https://placehold.co/600x400/cccccc/000000?text=Octaedro+V3+1%2F2" },
            "L3_3/8": { "3/8": "https://placehold.co/600x400/cccccc/000000?text=Octaedro+L3+3%2F8" },
            "L3_5/8": { "5/8": "https://placehold.co/600x400/cccccc/000000?text=Octaedro+L3+5%2F8" },
            "V4": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Octaedro+V4" },
            "V5": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Octaedro+V5" },
            "V6": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Octaedro+V6" }
        },
        "Dodecahedron": {
            "L1": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Dodecaedro+L1" },
            "L2": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Dodecaedro+L2" },
            "L2T": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Dodecaedro+L2T" }
        },
        "Tetrahedron": {
            "L2T": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Tetraedro+L2T" },
            "L3T": { "N/D": "https://placehold.co/600x400/cccccc/000000?text=Tetraedro+L3T" }
        }
    };

    // --- 1. CRIAR O HTML DA CALCULADORA ---
    const calculatorHTML = `
        <div id="calculator-fixed-box">
            <h2 id="calculator-title">Calculadora de Domos</h2>
            <form id="calculator-form-widget">
                <div class="form-group-widget">
                    <label for="diameter-widget">Diâmetro (m):</label>
                    <input type="number" id="diameter-input-widget" step="0.01" required>
                </div>
                <div class="form-group-widget">
                    <label for="base-solid-widget">Sólido Base:</label>
                    <select id="base-solid-input-widget"></select>
                </div>
                <div class="form-group-widget">
                    <label for="frequency-widget">Frequência/Variante:</label>
                    <select id="frequency-input-widget"></select>
                </div>
                <div class="form-group-widget">
                    <label for="truncation-widget">Tipo de Esfera:</label>
                    <select id="truncation-input-widget"></select>
                </div>
                <div class="form-group-widget">
                    <label for="pole-diameter-widget">Diâmetro das Varas (cm):</label>
                    <input type="number" id="pole-diameter-input-widget" step="0.01" value="5">
                </div>
                <div class="form-group-widget">
                    <label for="connector-cutoff-widget">Desconto Conector (cm):</label>
                    <input type="number" id="connector-cutoff-input-widget" step="0.01" value="2">
                </div>
                <button type="submit">Calcular</button>
            </form>
            <div id="results-container-widget" style="display: none; margin-top: 1rem;">
                <h4>resultados:</h4>
                <div id="results-table-widget"></div>
                <div id="material-costs-widget"></div>
                <div id="diagram-section-widget" style="display: none; text-align: center; margin-top: 15px;">
                    <img id="dome-diagram-img" src="" alt="Diagrama da Cúpula" style="max-width: 100%; height: auto; border-radius: 8px;">
                    <button id="view-diagram-button" style="margin-top: 10px; padding: 8px 15px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">Ver Diagrama Grande</button>
                </div>
            </div>
            <p id="error-message-widget" style="color: red;"></p>
        </div>

        <div id="diagram-modal" style="display: none; position: fixed; z-index: 1001; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.8);">
            <span class="close-button" id="close-diagram-modal" style="position: absolute; right: 25px; top: 15px; color: #f1f1f1; font-size: 40px; font-weight: bold; cursor: pointer;">&times;</span>
            <img class="modal-content" id="modal-diagram-img" style="margin: auto; display: block; width: 80%; max-width: 700px; border-radius: 8px;">
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', calculatorHTML);

    // --- 2. ADICIONAR ESTILOS CSS ---
    // Estilos para a calculadora e os novos elementos de imagem/modal
    const calculatorCSS = `#calculator-fixed-box{position:fixed;bottom:20px;right:20px;background-color:#fff;border:1px solid #ccc;border-radius:8px;padding:15px;box-shadow:0 4px 8px rgba(0,0,0,0.15);width:300px;z-index:1000;font-size:14px; max-height: calc(100vh - 40px); overflow-y: auto;} #calculator-fixed-box h2{font-size:1.1rem; margin-top:0; text-align:center;} .form-group-widget{margin-bottom:10px;} .form-group-widget label{display:block;margin-bottom:5px;font-weight:bold;} .form-group-widget input, .form-group-widget select{width:100%;padding:8px;box-sizing:border-box;} #results-container-widget h4{margin-top:15px;margin-bottom:10px;border-top:1px solid #eee;padding-top:10px;} #results-container-widget table{width:100%;border-collapse:collapse;font-size:13px;} #results-container-widget th, #results-container-widget td{border:1px solid #ddd;padding:5px;text-align:left;}
    #view-diagram-button { background-color: #007bff; }
    #view-diagram-button:hover { background-color: #0056b3; }
    #diagram-modal { display: none; position: fixed; z-index: 1001; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.8); }
    .modal-content { margin: auto; display: block; width: 80%; max-width: 700px; border-radius: 8px; animation-name: zoom; animation-duration: 0.6s; }
    .close-button { position: absolute; right: 25px; top: 15px; color: #f1f1f1; font-size: 40px; font-weight: bold; cursor: pointer; }
    .close-button:hover, .close-button:focus { color: #bbb; text-decoration: none; cursor: pointer; }
    @keyframes zoom { from {transform: scale(0)} to {transform: scale(1)} }`;
    const styleSheet = document.createElement("style");
    styleSheet.innerText = calculatorCSS;
    document.head.appendChild(styleSheet);

    // --- 3. LÓGICA E INTERATIVIDADE ---
    const calculatorForm = document.getElementById('calculator-form-widget');
    const solidSelect = document.getElementById('base-solid-input-widget');
    const freqSelect = document.getElementById('frequency-input-widget');
    const truncSelect = document.getElementById('truncation-input-widget');
    const poleDiameterInput = document.getElementById('pole-diameter-input-widget');
    const connectorCutoffInput = document.getElementById('connector-cutoff-input-widget');
    const resultsContainer = document.getElementById('results-container-widget');
    const resultsTableDiv = document.getElementById('results-table-widget');
    const materialCostsDiv = document.getElementById('material-costs-widget');
    const errorMessageP = document.getElementById('error-message-widget');
    const diagramSection = document.getElementById('diagram-section-widget');
    const domeDiagramImg = document.getElementById('dome-diagram-img');
    const viewDiagramButton = document.getElementById('view-diagram-button');
    const diagramModal = document.getElementById('diagram-modal');
    const modalDiagramImg = document.getElementById('modal-diagram-img');
    const closeDiagramModal = document.getElementById('close-diagram-modal');

    const apiUrl = 'https://us-central1-adroit-citadel-397215.cloudfunctions.net/calculadora-domo-api';

    // Funções para popular os menus suspensos
    function populateSelect(selectElement, options) {
        selectElement.innerHTML = '';
        options.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option;
            opt.textContent = option;
            selectElement.appendChild(opt);
        });
    }

    function updateFreqOptions() {
        const selectedSolid = solidSelect.value;
        const freqs = Object.keys(DOME_DATA[selectedSolid] || {});
        populateSelect(freqSelect, freqs);
        updateTruncOptions();
    }

    function updateTruncOptions() {
        const selectedSolid = solidSelect.value;
        const selectedFreq = freqSelect.value;
        
        let truncs = [];
        // ATUALIZADO: Acessa diretamente as chaves do objeto 'truncation' para obter as opções de truncagem
        if (DOME_DATA[selectedSolid]?.[selectedFreq]?.truncation) {
            truncs = Object.keys(DOME_DATA[selectedSolid][selectedFreq].truncation);
        }
        
        populateSelect(truncSelect, truncs);
        
        // Garante que uma opção válida seja selecionada para evitar estados inválidos
        if (truncs.length > 0) {
            truncSelect.value = truncs[0];
        } else {
            truncSelect.value = ''; 
        }

        updateDiagramImage();
    }

    // Função para atualizar a imagem do diagrama
    function updateDiagramImage() {
        const selectedSolid = solidSelect.value;
        const selectedFreq = freqSelect.value;
        const selectedTrunc = truncSelect.value;

        // Se selectedTrunc estiver vazio (por exemplo, quando não há truncagens), tentamos pegar a primeira disponível no DOME_IMAGES
        const imageUrl = DOME_IMAGES[selectedSolid]?.[selectedFreq]?.[selectedTrunc] ||
                         (selectedTrunc === '' && Object.keys(DOME_IMAGES[selectedSolid]?.[selectedFreq] || {}).length > 0
                            ? DOME_IMAGES[selectedSolid][selectedFreq][Object.keys(DOME_IMAGES[selectedSolid][selectedFreq])[0]]
                            : undefined);

        if (imageUrl) {
            domeDiagramImg.src = imageUrl;
            diagramSection.style.display = 'block';
        } else {
            diagramSection.style.display = 'none';
            domeDiagramImg.src = '';
        }
    }

    // Lógica de submissão do formulário
    calculatorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        resultsContainer.style.display = 'none';
        errorMessageP.textContent = '';
        materialCostsDiv.innerHTML = '';
        diagramSection.style.display = 'none';

        const diameter = parseFloat(document.getElementById('diameter-input-widget').value);
        const base_solid = solidSelect.value;
        const frequency = freqSelect.value;
        const truncation = truncSelect.value; 

        let poleDiameterCm = parseFloat(poleDiameterInput.value);
        let connectorCutoffCm = parseFloat(connectorCutoffInput.value);

        if (isNaN(poleDiameterCm) || poleDiameterCm <= 0) {
            poleDiameterCm = "N/A";
        }
        if (isNaN(connectorCutoffCm) || connectorCutoffCm < 0) {
            connectorCutoffCm = "N/A";
        }

        const payload = {
            diameter: diameter,
            base_solid: base_solid,
            frequency: frequency,
            truncation: truncation
        };

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            const data = await response.json();
            if (data.success) {
                displayResults(data, diameter, poleDiameterCm, connectorCutoffCm);
                updateDiagramImage();
            } else {
                errorMessageP.textContent = data.error || 'Ocorreu um erro.';
            }
        } catch (error) {
            errorMessageP.textContent = 'Erro de comunicação com a API: ' + error.message;
        }
        resultsContainer.style.display = 'block';
    });

    function displayResults(data, domeDiameter, poleDiameterCm, connectorCutoffCm) {
        let tableHTML = '<table><thead><tr><th>Tipo</th><th>Comp. Final (m)</th><th>Qtd.</th><th>Ângulo (\u03B1)</th></tr></thead><tbody>';
        let totalLinearMeters = 0;
        let totalSegments = 0;

        for (const key in data.segment_lengths) {
            const calculatedLength = parseFloat(data.segment_lengths[key]);
            const quantity = data.num_segments[key];
            const vertexAngle = data.vertex_angles[key];

            let finalLengthM;
            if (typeof connectorCutoffCm === 'number') {
                finalLengthM = calculatedLength - (connectorCutoffCm / 100); 
            } else {
                finalLengthM = calculatedLength;
            }
            
            totalLinearMeters += finalLengthM * quantity;
            totalSegments += quantity;

            tableHTML += `<tr><td>${key}</td><td>${typeof finalLengthM === 'number' ? finalLengthM.toFixed(4) : 'N/A'}</td><td>${quantity}</td><td>${vertexAngle !== 'N/D' ? vertexAngle.toFixed(2) + '\u00B0' : 'N/A'}</td></tr>`;
        }
        tableHTML += '</tbody></table>';
        resultsTableDiv.innerHTML = tableHTML;

        let materialHTML = '<h4>Custos de Materiais:</h4><ul>';

        const selectedSolid = solidSelect.value;
        const selectedFreq = freqSelect.value;
        const selectedTrunc = truncSelect.value;

        let numVertices = DOME_DATA[selectedSolid]?.[selectedFreq]?.total_vertices;
        if (typeof numVertices === 'object' && numVertices !== null) {
            numVertices = numVertices[selectedTrunc];
        }


        materialHTML += `<li>Número de Vértices: ${numVertices}</li>`;
        materialHTML += `<li>Total de Metros Lineares de Varas de Bambu: ${totalLinearMeters.toFixed(2)} m</li>`;
        materialHTML += `<li>Número de Conectores Utilizados: ${totalSegments} (1 por extremidade da vara)</li>`;

        materialHTML += `<h5>Materiais por Vara (Baseado no total de varas):</h5><ul>`;
        materialHTML += `<li>Número de Sapatilhas: ${totalSegments * 2}</li>`;
        materialHTML += `<li>Cabo de Aço: ${totalSegments * 2} m</li>`;
        materialHTML += `<li>Prensa Cabo: ${totalSegments * 4}</li>`;
        materialHTML += `<li>Arruelas: ${totalSegments * 4}</li>`;

        let puUg132aMl = 0;
        if (typeof poleDiameterCm === 'number') {
            if (poleDiameterCm > 0 && poleDiameterCm <= 5) {
                puUg132aMl = 30 * totalLinearMeters;
            } else if (poleDiameterCm > 5 && poleDiameterCm <= 10) {
                puUg132aMl = 60 * totalLinearMeters;
            }
        }
        materialHTML += `<li>PU Vegetal UG132A: ${typeof puUg132aMl === 'number' && puUg132aMl > 0 ? puUg132aMl.toFixed(2) + ' ml' : 'N/A'}</li>`;

        let puMamonexMl = 0;
        if (typeof poleDiameterCm === 'number') {
            if (poleDiameterCm > 0 && poleDiameterCm <= 5) {
                puMamonexMl = 100 * totalSegments;
            } else if (poleDiameterCm > 5 && poleDiameterCm <= 10) {
                puMamonexMl = 150 * totalSegments;
            }
        }
        materialHTML += `<li>PU Vegetal Mamonex RD70: ${typeof puMamonexMl === 'number' && puMamonexMl > 0 ? puMamonexMl.toFixed(2) + ' ml' : 'N/A'}</li>`;

        const vertexDiameterCm = typeof poleDiameterCm === 'number' && poleDiameterCm > 0 ? (poleDiameterCm * 2) : 'N/A';
        materialHTML += `<li>Diâmetro dos Vértices (estimado): ${vertexDiameterCm} cm</li>`;
        materialHTML += `<li>Número de Anéis de Borracha: ${typeof numVertices === 'number' ? numVertices * 2 : 'N/A'}</li>`;
        materialHTML += `</ul>`;

        materialHTML += '</ul>';
        materialCostsDiv.innerHTML = materialHTML;
    }

    // Inicializa o formulário e a exibição da imagem
    populateSelect(solidSelect, Object.keys(DOME_DATA));
    updateFreqOptions(); 

    // Funcionalidade do Modal
    viewDiagramButton.addEventListener('click', () => {
        modalDiagramImg.src = domeDiagramImg.src;
        diagramModal.style.display = 'block';
    });

    closeDiagramModal.addEventListener('click', () => {
        diagramModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == diagramModal) {
            diagramModal.style.display = 'none'; // CORRIGIDO AQUI!
        }
    });
});
