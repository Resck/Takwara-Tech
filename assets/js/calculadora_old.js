
// docs/assets/js/calculadora.js - VERSÃO FINAL COMPLETA COM IMAGENS E MODAL (REVISADA)

if (window.location.pathname.startsWith('/calculadora/')) {
document.addEventListener('DOMContentLoaded', () => {

    // A base de dados que o seu backend usa para popular os menus dinamicamente.
    const DOME_DATA = {
        "Icosahedron": {
            "V1": {"truncation": {"2/3": {}}},
            "V2": {"truncation": {"1/2": {}}},
            "V3": {"truncation": {"3/8": {}, "5/8": {}}},
            "V4": {"truncation": {"1/2": {}}},
            "L3": {"truncation": {"1/2": {}}},
            "V5": {"truncation": {"7/15": {}, "8/15": {}}},
            "V6": {"truncation": {"1/2": {}}},
            "2V.3V": {"truncation": {"1/2": {}}}
        },
        "Cube": {
            "V1": {"truncation": {"N/D": {}}},
            "V2": {"truncation": {"N/D": {}}},
            "V3": {"truncation": {"N/D": {}}},
            "V4": {"truncation": {"N/D": {}}},
            "V5": {"truncation": {"~1/2": {}}},
            "V6": {"truncation": {"1/2": {}}},
            "2V.3V": {"truncation": {"1/2": {}}},
            "3V.2V": {"truncation": {"1/2": {}}}
        },
        "Octahedron": {
            "V1": {"truncation": {"1/2": {}}},
            "V2": {"truncation": {"1/2": {}}},
            "V3": {"truncation": {"1/2": {}}},
            "L3_3/8": {"truncation": {"3/8": {}}},
            "L3_5/8": {"truncation": {"5/8": {}}},
            "V4": {"truncation": {"N/D": {}}},
            "V5": {"truncation": {"N/D": {}}},
            "V6": {"truncation": {"N/D": {}}}
        },
        "Dodecahedron": {
            "L1": {"truncation": {"N/D": {}}},
            "L2": {"truncation": {"N/D": {}}},
            "L2T": {"truncation": {"N/D": {}}}
        },
        "Tetrahedron": {
            "L2T": {"truncation": {"N/D": {}}},
            "L3T": {"truncation": {"N/D": {}}}
        }
    };

    // Nova base de dados para URLs de imagens de diagramas
    const DOME_IMAGES = {
        "Icosahedron": {
            "V1": { "2/3": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+V1+2%2F3" },
            "V2": { "1/2": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+V2+1%2F2" },
            "V3": {
                "3/8": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+V3+3%2F8",
                "5/8": "https://placehold.co/600x400/cccccc/000000?text=Icosaedro+V3+5%2F8"
            },
            "V4": { "1/2": "uploaded:image_53a331.png-3bd87591-3b88-43d9-99ea-14781c806ce2" },
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
                <small id="pole-diameter-note" style="display: none; color: gray; font-size: 0.8em; margin-top: 5px;">Se não preenchido, o cálculo de PU e Cabo de Aço será N/A ou padrão.</small>
            </div>
            <button type="submit" id="calculate-button">Calcular</button>
        </form>
        <div id="results-container-widget" style="margin-top: 1rem;">
            <h4>resultados:</h4>
            <div id="results-table-widget"></div>
            <div id="material-costs-widget"></div>
            <div id="diagram-section-widget" style="display: none; text-align: center; margin-top: 15px;">
                <img id="dome-diagram-img" src="" alt="Diagrama da Cúpula" style="max-width: 100%; height: auto; border-radius: 8px;">
                <button id="view-diagram-button" style="margin-top: 10px; padding: 8px 15px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">Ver Diagrama Grande</button>
            </div>
            <button id="download-results-button" style="margin-top: 15px; padding: 10px 20px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; display: none;">Baixar Resultados (.md)</button>
        </div>
        <p id="error-message-widget" style="color: red;"></p>
        <p id="footer-notes" style="font-size: 0.8em; color: gray; margin-top: 15px; display: none;"></p>
    </div>

    <div id="diagram-modal" style="display: none; position: fixed; z-index: 1001; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.8);">
        <span class="close-button" id="close-diagram-modal" style="position: absolute; right: 25px; top: 15px; color: #f1f1f1; font-size: 40px; font-weight: bold; cursor: pointer;">&times;</span>
        <img class="modal-content" id="modal-diagram-img" style="margin: auto; display: block; width: 80%; max-width: 700px; border-radius: 8px;">
    </div>
    `;
    document.body.insertAdjacentHTML('beforeend', calculatorHTML);

    // --- 2. ADICIONAR ESTILOS CSS ---
    const calculatorCSS = `#calculator-fixed-box{position:fixed;bottom:20px;right:20px;background-color:#fff;border:1px solid #ccc;border-radius:8px;padding:15px;box-shadow:0 4px 8px rgba(0,0,0,0.15);width:500px;z-index:1000;font-size:14px; max-height: calc(100vh - 40px); overflow-y: auto;} #calculator-fixed-box h2{font-size:1.1rem; margin-top:0; text-align:center;} .form-group-widget{margin-bottom:10px;} .form-group-widget label{display:block;margin-bottom:5px;font-weight:bold;} .form-group-widget input, .form-group-widget select{width:100%;padding:8px;box-sizing:border-box;} #results-container-widget h4{margin-top:15px;margin-bottom:10px;border-top:1px solid #eee;padding-top:10px;} #results-container-widget table{width:100%;border-collapse:collapse;font-size:13px;} #results-container-widget th, #results-container-widget td{border:1px solid #ddd;padding:5px;text-align:left;}

    #calculate-button { /* Destaque para o botão Calcular */
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3); /* Sombra para destacar */
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
        width: 100%;
        margin-top: 10px;
    }
    #calculate-button:hover {
        background-color: #0056b3;
        box-shadow: 0 6px 12px rgba(0, 123, 255, 0.4);
    }

    #view-diagram-button { background-color: #007bff; }
    #view-diagram-button:hover { background-color: #0056b3; }

    #download-results-button:hover { background-color: #218838; }

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
    const poleDiameterNote = document.getElementById('pole-diameter-note');
    const downloadResultsButton = document.getElementById('download-results-button');
    const footerNotes = document.getElementById('footer-notes');

    // Variáveis para armazenar os dados da última simulação para o download
    let lastCalculatedData = null;
    let lastSelectedSolid = '';
    let lastSelectedFreq = '';
    let lastSelectedTrunc = '';
    let lastPoleDiameterCm = 'N/A';
    let lastTotalLinearMeters = 0;


    // Substitua pela sua URL da API, se for diferente
    const apiUrl = 'https://southamerica-east1-adroit-citadel-397215.cloudfunctions.net/calculadora-domo-api'; // URL da API atualizada


    // Funções para popular os menus suspensos
    function populateSelect(selectElement, options) {
        selectElement.innerHTML = '';
        if (options.length === 0) {
            const opt = document.createElement('option');
            opt.value = "";
            opt.textContent = "N/D";
            selectElement.appendChild(opt);
            selectElement.disabled = true;
        } else {
            selectElement.disabled = false;
            options.forEach(option => {
                const opt = document.createElement('option');
                opt.value = option;
                opt.textContent = option;
                selectElement.appendChild(opt);
            });
        }
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

        if (DOME_DATA[selectedSolid]?.[selectedFreq]?.truncation) {
            truncs = Object.keys(DOME_DATA[selectedSolid][selectedFreq].truncation);
        }
        populateSelect(truncSelect, truncs);

        if (truncs.length > 0) {
            truncSelect.value = truncs[0];
        } else {
            truncSelect.value = '';
        }

        updateDiagramImage();
    }

    function updateDiagramImage() {
        const selectedSolid = solidSelect.value;
        const selectedFreq = freqSelect.value;
        const selectedTrunc = truncSelect.value;

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

    // Função de arredondamento personalizada: arredonda para 2 casas decimais.
    // O arredondamento padrão do toFixed() já é "round half up", o que é o mais comum.
    // Ex: 1.235 -> 1.24, 1.234 -> 1.23.
    // Se a intenção é estritamente que X.YY5 -> X.YY e X.YY6 -> X.Y(Y+1),
    // a lógica precisaria ser mais complexa (como a versão anterior).
    // Para simplificar, vou usar o padrão JS de arredondar toFixed(2).
    function customRound(value) {
        if (typeof value !== 'number' || isNaN(value)) {
            return 'N/A';
        }
        // Arredonda para 2 casas decimais usando Math.round para evitar problemas de ponto flutuante
        return (Math.round(value * 100) / 100).toFixed(2);
    }


    calculatorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        resultsContainer.style.display = 'none';
        errorMessageP.textContent = '';
        materialCostsDiv.innerHTML = '';
        diagramSection.style.display = 'none';
        downloadResultsButton.style.display = 'none';
        footerNotes.style.display = 'none';

        const diameter = parseFloat(document.getElementById('diameter-input-widget').value);
        const base_solid = solidSelect.value;
        const frequency = freqSelect.value;
        const truncation = truncSelect.value;

        let poleDiameterCm = parseFloat(poleDiameterInput.value);
        
        if (isNaN(parseFloat(poleDiameterInput.value)) || parseFloat(poleDiameterInput.value) <= 0) {
            poleDiameterCm = "N/A";
            poleDiameterNote.style.display = 'block';
        } else {
            poleDiameterNote.style.display = 'none';
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
            
            console.log("Dados da API:", data); 

            if (data.success) {
                // Cálculo do desconto da conexão: 2 * (metade do diâmetro do vértice)
                const SPACING_MM = 4;
                const SPACING_CM = SPACING_MM / 10;
                let connectorCutoffValueCm = 0; // O valor da metade do diâmetro do vértice em cm
                let actualConnectorCutoffMeters = 0; // O valor total do desconto em metros (para as duas extremidades)

                if (typeof poleDiameterCm === 'number' && poleDiameterCm > 0) {
                    const calculatedVertexDiameter = 2 * (1.5 * poleDiameterCm + SPACING_CM);
                    connectorCutoffValueCm = (calculatedVertexDiameter / 2); // Metade do diâmetro do vértice em cm
                    actualConnectorCutoffMeters = (2 * connectorCutoffValueCm / 100); // Duas extremidades em metros
                }
                
                let totalLinearMetersCalculated = 0;
                let totalSegmentsCalculated = 0;
                let segmentResultsForDisplay = []; // Para armazenar resultados após o desconto

                for (const key in data.segment_lengths) {
                    const originalLength = parseFloat(data.segment_lengths[key]);
                    const quantity = data.num_segments[key];
                    const vertexAngle = data.vertex_angles[key];

                    // Aplica o desconto da conexão
                    let finalLengthM = originalLength - actualConnectorCutoffMeters;

                    totalLinearMetersCalculated += finalLengthM * quantity;
                    totalSegmentsCalculated += quantity;

                    segmentResultsForDisplay.push({
                        type: key,
                        originalLength: originalLength,
                        discount: actualConnectorCutoffMeters,
                        finalLength: finalLengthM,
                        quantity: quantity,
                        angle: vertexAngle
                    });
                }
                // --- REMOVIDA LÓGICA DE ORDENAÇÃO E AJUSTE DE 1CM ---
                // Não é mais necessária, dado que a flexibilidade da conexão absorve pequenas variações.
                
                lastTotalLinearMeters = totalLinearMetersCalculated; // Armazena o total linear ajustado
                
                // Armazena segmentResultsForDisplay para o Markdown
                lastCalculatedData = { ...data, segmentResultsForDisplay: segmentResultsForDisplay };

                displayResults(data, diameter, poleDiameterCm, totalLinearMetersCalculated, totalSegmentsCalculated, segmentResultsForDisplay);
                updateDiagramImage();
                downloadResultsButton.style.display = 'block';

                lastSelectedSolid = base_solid;
                lastSelectedFreq = frequency;
                lastSelectedTrunc = truncation;
                lastPoleDiameterCm = poleDiameterCm;

            } else {
                errorMessageP.textContent = data.error || 'Ocorreu um erro.';
            }
        } catch (error) {
            errorMessageP.textContent = 'Erro de comunicação com a API: ' + error.message;
        }
        resultsContainer.style.display = 'block';
    });

    function displayResults(data, domeDiameter, poleDiameterCm, totalLinearMeters, totalSegments, segmentResultsForDisplay) {
        // Atualiza cabeçalhos da tabela com as novas colunas
        let tableHTML = '<table><thead><tr><th>Tipo</th><th>Comp. Original (m)</th><th>Desconto Conector (m)</th><th>Comp. Final (m)</th><th>Qtd.</th><th>Ângulo (\u03B1)</th></tr></thead><tbody>';
        
        segmentResultsForDisplay.forEach(segment => {
            // Aplica a função de arredondamento personalizada para todas as colunas de comprimento
            const originalLengthRounded = customRound(segment.originalLength);
            const discountRounded = customRound(segment.discount);
            const finalLengthRounded = customRound(segment.finalLength); 

            tableHTML += `<tr><td>${segment.type}</td><td>${originalLengthRounded}</td><td>${discountRounded}</td><td>${finalLengthRounded}</td><td>${segment.quantity}</td><td>${segment.angle !== 'N/D' ? segment.angle.toFixed(2) + '\u00B0' : 'N/A'}</td></tr>`;
        });

        tableHTML += '</tbody></table>';
        resultsTableDiv.innerHTML = tableHTML;

        // ** Recursos Materiais **
        let materialHTML = '<h4>Recursos Materiais:</h4><ul>';

        // Garante que numVertices seja um número ou "N/A"
        const numVertices = typeof data.total_vertices === 'number' ? data.total_vertices : 'N/A'; 

        materialHTML += `<li>Número de Vértices: ${numVertices}</li>`;
        materialHTML += `<li>Número Total de Varas: ${totalSegments}</li>`;
        materialHTML += `<li>Total de Metros Lineares de Varas de Bambu: ${totalLinearMeters.toFixed(2)} m</li>`; // Total linear já reflete os ajustes
        
        const numConectores = totalSegments * 2;
        materialHTML += `<li>Número de Conectores Utilizados: ${numConectores} (2 por vara)</li>`;

        // Lógica para Cabo de Aço
        let cableLengthPerRod = 2; // 1m por extremidade, 2m por vara (padrão)
        if (typeof poleDiameterCm === 'number' && poleDiameterCm >= 6.5) {
            cableLengthPerRod = 3; // 1.5m por extremidade, 3m por vara
        }
        const totalCableLength = totalSegments * cableLengthPerRod;

        materialHTML += `<li>Cabo de Aço: ${totalCableLength} m</li>`;
        materialHTML += `<li>Número de Sapatilhas: ${totalSegments * 2}</li>`;
        materialHTML += `<li>Prensa Cabo: ${totalSegments * 4}</li>`;
        materialHTML += `<li>Arruelas: ${totalSegments * 4}</li>`;
        materialHTML += `<li>Parafusos com Porcas: ${numConectores}</li>`;

        // Lógica para PU Vegetal UG132A
        let puUg132aMl = 0;
        if (typeof poleDiameterCm === 'number') {
            if (poleDiameterCm > 0 && poleDiameterCm <= 5) {
                puUg132aMl = 30 * totalLinearMeters; // Usa totalLinearMeters já ajustado
            } else if (poleDiameterCm > 5 && poleDiameterCm <= 10) {
                puUg132aMl = 60 * totalLinearMeters; // Usa totalLinearMeters já ajustado
            }
        }
        const displayPuUg132a = puUg132aMl >= 1000 ? `${(puUg132aMl / 1000).toFixed(2)} L` : `${puUg132aMl.toFixed(2)} ml`;
        materialHTML += `<li>PU Vegetal UG132A: ${typeof puUg132aMl === 'number' && puUg132aMl > 0 ? displayPuUg132a : 'N/A'}</li>`;

        // Lógica para PU Vegetal Mamonex RD70
        let puMamonexMl = 0;
        if (typeof poleDiameterCm === 'number') {
            if (poleDiameterCm > 0 && poleDiameterCm <= 5) {
                puMamonexMl = 100 * totalSegments;
            } else if (poleDiameterCm > 5 && poleDiameterCm <= 10) {
                puMamonexMl = 150 * totalSegments;
            }
        }
        const displayPuMamonex = puMamonexMl >= 1000 ? `${(puMamonexMl / 1000).toFixed(2)} L` : `${puMamonexMl.toFixed(2)} ml`;
        materialHTML += `<li>PU Vegetal Mamonex RD70: ${typeof puMamonexMl === 'number' && puMamonexMl > 0 ? displayPuMamonex : 'N/A'}</li>`;

        // ** CÁLCULO ATUALIZADO PARA DIÂMETRO DOS VÉRTICES (0.4cm espaçamento) **
        let vertexDiameterDisplay = 'N/A';
        let connectorLengthCm = 'N/A';
        const SPACING_MM = 4; // 4mm de espaçamento
        const SPACING_CM = SPACING_MM / 10; // Converte para cm

        if (typeof poleDiameterCm === 'number' && poleDiameterCm > 0) {
            // Fórmula: 2 * (1.5 * D + espaçamento_cm)
            const calculatedVertexDiameter = 2 * (1.5 * poleDiameterCm + SPACING_CM);
            vertexDiameterDisplay = calculatedVertexDiameter.toFixed(2) + ' cm';
            connectorLengthCm = (calculatedVertexDiameter / 2).toFixed(2); // Comprimento do conector = 1/2 do diâmetro do vértice
        }
        materialHTML += `<li>Diâmetro dos Vértices (estimado): ${vertexDiameterDisplay}</li>`;

        materialHTML += `<li>Número de Anéis de Borracha: ${typeof numVertices === 'number' ? numVertices : 'N/A'}</li>`;
        materialHTML += `</ul>`;
        materialCostsDiv.innerHTML = materialHTML;

        // ** Observações no Rodapé **
        let notesHTML = `
            <p><strong>Observações:</strong></p>
            <ul>
                <li>Diâmetro das Varas: ${typeof poleDiameterCm === 'number' ? poleDiameterCm + ' cm' : 'Não informado. O cálculo de PU e Cabo de Aço pode ser afetado.'}</li>
                <li>O cálculo do diâmetro dos vértices (${vertexDiameterDisplay}) considera uma união de 6 varas dispostas circularmente, cada uma com o diâmetro da vara, e com um espaçamento de ${SPACING_MM}mm entre elas. Este diâmetro define o comprimento do conector, que é metade do diâmetro do vértice (${connectorLengthCm} cm), e é crucial para evitar colapsos estruturais.</li>
                <li>A especificação do cabo de aço será determinada pela carga solicitada, espécie e diâmetro do bambu a ser utilizado.</li>
                <li>Os furos nas varas de bambu para a passagem do cabo devem ser feitos nas extremidades a um ângulo de 45° no sentido da entrada, com diâmetro correspondente à espessura do cabo.</li>
                <li>Serão realizados dois furos perpendiculares a 3cm da extremidade e dois furos perpendiculares a 5cm da extremidade.</li>
                <li>A especificação de parafusos com porcas pode variar de acordo com o esforço e peso recebido pela estrutura. Consulte um engenheiro.</li>
            </ul>
        `;
        footerNotes.innerHTML = notesHTML;
        footerNotes.style.display = 'block';
    }

    // Função para gerar o arquivo Markdown
    function generateMarkdown() {
        const diameter = document.getElementById('diameter-input-widget').value;
        const base_solid = lastSelectedSolid;
        const frequency = lastSelectedFreq;
        const truncation = lastSelectedTrunc;
        const poleDiameterCm = lastPoleDiameterCm;
        const data = lastCalculatedData;
        const totalLinearMetersMd = lastTotalLinearMeters;
        const totalSegmentsMd = data.total_segments;

        const diagramImageUrl = domeDiagramImg.src;

        let markdownContent = `# Resultados da Calculadora de Domos\n\n`;
        markdownContent += `## Detalhes do Domo\n`;
        markdownContent += `- **Sólido Base:** ${base_solid}\n`;
        markdownContent += `- **Frequência/Variante:** ${frequency}\n`;
        markdownContent += `- **Tipo de Esfera (Truncagem):** ${truncation}\n`;
        markdownContent += `- **Diâmetro do Domo:** ${diameter} m\n`;
        markdownContent += `- **Diâmetro das Varas:** ${typeof poleDiameterCm === 'number' ? poleDiameterCm + ' cm' : 'N/A (Cálculo de PU e Cabo de Aço pode ser afetado)'}\n`;
        markdownContent += `\n`;

        markdownContent += `## Comprimento dos Segmentos\n\n`;
        // Recria a tabela para o Markdown com base nos dados já processados com desconto e arredondamento
        markdownContent += `| Tipo | Comp. Original (m) | Desconto Conector (m) | Comp. Final (m) | Qtd. | Ângulo (α) |\n`; // Novos cabeçalhos
        markdownContent += `|---|---|---|---|---|---|\n`; // Novas divisões
        lastCalculatedData.segmentResultsForDisplay.forEach(segment => { // Use os dados armazenados
            markdownContent += `| ${segment.type} | ${customRound(segment.originalLength)} | ${customRound(segment.discount)} | ${customRound(segment.finalLength)} | ${segment.quantity} | ${segment.angle !== 'N/D' ? segment.angle.toFixed(2) + '°' : 'N/A'} |\n`;
        });
        markdownContent += `\n`;

        // **Recursos Materiais para o MD**
        markdownContent += `## Recursos Materiais\n\n`;

        const numVerticesMd = typeof data.total_vertices === 'number' ? data.total_vertices : 'N/A';

        markdownContent += `- Número de Vértices: ${numVerticesMd}\n`;
        markdownContent += `- Número Total de Varas: ${totalSegmentsMd}\n`;
        markdownContent += `- Total de Metros Lineares de Varas de Bambu: ${typeof totalLinearMetersMd === 'number' ? totalLinearMetersMd.toFixed(2) : 'N/A'} m\n`;
        
        const numConectoresMd = totalSegmentsMd * 2;
        markdownContent += `- Número de Conectores Utilizados: ${numConectoresMd} (2 por vara)\n`;

        let cableLengthPerRodMd = 2;
        if (typeof poleDiameterCm === 'number' && poleDiameterCm >= 6.5) {
            cableLengthPerRodMd = 3;
        }
        const totalCableLengthMd = totalSegmentsMd * cableLengthPerRodMd;
        markdownContent += `- Cabo de Aço: ${typeof totalCableLengthMd === 'number' ? totalCableLengthMd : 'N/A'} m\n`;

        markdownContent += `- Número de Sapatilhas: ${typeof totalSegmentsMd === 'number' ? totalSegmentsMd * 2 : 'N/A'}\n`;
        markdownContent += `- Prensa Cabo: ${typeof totalSegmentsMd === 'number' ? totalSegmentsMd * 4 : 'N/A'}\n`;
        markdownContent += `- Arruelas: ${typeof totalSegmentsMd === 'number' ? totalSegmentsMd * 4 : 'N/A'}\n`;
        markdownContent += `- Parafusos com Porcas: ${typeof numConectoresMd === 'number' ? numConectoresMd : 'N/A'}\n`;

        // PU para MD
        let puUg132aMlMd = 0;
        if (typeof poleDiameterCm === 'number') {
            if (poleDiameterCm > 0 && poleDiameterCm <= 5) {
                puUg132aMlMd = 30 * totalLinearMetersMd;
            } else if (poleDiameterCm > 5 && poleDiameterCm <= 10) {
                puUg132aMlMd = 60 * totalLinearMetersMd;
            }
        }
        const displayPuUg132aMd = puUg132aMlMd >= 1000 ? `${(puUg132aMlMd / 1000).toFixed(2)} L` : `${puUg132aMlMd.toFixed(2)} ml`;
        markdownContent += `- PU Vegetal UG132A: ${typeof puUg132aMlMd === 'number' && puUg132aMlMd > 0 ? displayPuUg132aMd : 'N/A'}\n`;

        let puMamonexMlMd = 0;
        if (typeof poleDiameterCm === 'number') {
            if (poleDiameterCm > 0 && poleDiameterCm <= 5) {
                puMamonexMlMd = 100 * totalSegmentsMd;
            } else if (poleDiameterCm > 5 && poleDiameterCm <= 10) {
                puMamonexMlMd = 150 * totalSegmentsMd;
            }
        }
        const displayPuMamonexMd = puMamonexMlMd >= 1000 ? `${(puMamonexMlMd / 1000).toFixed(2)} L` : `${puMamonexMlMd.toFixed(2)} ml`;
        markdownContent += `- PU Vegetal Mamonex RD70: ${typeof puMamonexMlMd === 'number' && puMamonexMlMd > 0 ? displayPuMamonexMd : 'N/A'}\n`;

        // Diâmetro dos Vértices para MD
        let vertexDiameterDisplayMd = 'N/A';
        let connectorLengthCmMd = 'N/A';
        const SPACING_MM_MD = 4;
        const SPACING_CM_MD = SPACING_MM_MD / 10;
        if (typeof poleDiameterCm === 'number' && poleDiameterCm > 0) {
            const calculatedVertexDiameterMd = 2 * (1.5 * poleDiameterCm + SPACING_CM_MD);
            vertexDiameterDisplayMd = calculatedVertexDiameterMd.toFixed(2) + ' cm';
            connectorLengthCmMd = (calculatedVertexDiameterMd / 2).toFixed(2);
        }
        markdownContent += `- Diâmetro dos Vértices (estimado): ${vertexDiameterDisplayMd}\n`;

        markdownContent += `- Número de Anéis de Borracha: ${typeof numVerticesMd === 'number' ? numVerticesMd : 'N/A'}\n\n`;

        if (diagramImageUrl && diagramImageUrl !== '') {
            markdownContent += `## Diagrama da Cúpula\n\n`;
            markdownContent += `![Diagrama da Cúpula](${diagramImageUrl})\n\n`;
            markdownContent += `*Para visualizar o diagrama em alta resolução, acesse a URL da imagem diretamente.*\n`;
        }

        markdownContent += `\n---\n\n`;
        markdownContent += `## Observações\n`;
        markdownContent += `- Diâmetro das Varas: ${typeof poleDiameterCm === 'number' ? poleDiameterCm + ' cm' : 'Não informado. O cálculo de PU e Cabo de Aço pode ser afetado.'}\n`;
        markdownContent += `- O cálculo do diâmetro dos vértices (${vertexDiameterDisplayMd}) considera uma união de 6 varas dispostas circularmente, cada uma com o diâmetro da vara, e com um espaçamento de ${SPACING_MM_MD}mm entre elas. Este diâmetro define o comprimento do conector, que é metade do diâmetro do vértice (${connectorLengthCmMd} cm), e é crucial para evitar colapsos estruturais.\n`;
        markdownContent += `- A especificação do cabo de aço será determinada pela carga solicitada, espécie e diâmetro do bambu a ser utilizado.\n`;
        markdownContent += `- Os furos nas varas de bambu para a passagem do cabo devem ser feitos nas extremidades a um ângulo de 45° no sentido da entrada, com diâmetro correspondente à espessura do cabo.\n`;
        markdownContent += `- Serão realizados dois furos perpendiculares a 3cm da extremidade e dois furos perpendiculares a 5cm da extremidade.\n`;
        markdownContent += `- A especificação de parafusos com porcas pode variar de acordo com o esforço e peso recebido pela estrutura. Consulte um engenheiro.\n`;

        return markdownContent;
    }

    downloadResultsButton.addEventListener('click', () => {
        if (!lastCalculatedData) {
            errorMessageP.textContent = 'Por favor, execute um cálculo antes de baixar os resultados.';
            return;
        }
        const markdown = generateMarkdown();
        const filename = `resultados_domo_${lastSelectedSolid.replace(/\s/g, '_')}_${lastSelectedFreq.replace(/\//g, '-')}_${lastSelectedTrunc.replace(/\//g, '-')}.md`;
        const blob = new Blob([markdown], { type: 'text/markdown;charset=utf-8;' });
        const link = document.createElement('a');
        if (link.download !== undefined) {
            link.setAttribute('href', URL.createObjectURL(blob));
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            alert('Seu navegador não suporta o download automático. Copie o texto abaixo:\n\n' + markdown);
        }
    });

    // Inicializa o formulário e a exibição da imagem
    populateSelect(solidSelect, Object.keys(DOME_DATA));
    solidSelect.addEventListener('change', updateFreqOptions);
    freqSelect.addEventListener('change', updateTruncOptions);
    truncSelect.addEventListener('change', updateDiagramImage);

    updateFreqOptions();

    // Event listeners para as notas de N/A nos campos de entrada
    poleDiameterInput.addEventListener('input', () => {
        if (isNaN(parseFloat(poleDiameterInput.value)) || parseFloat(poleDiameterInput.value) <= 0) {
            poleDiameterNote.style.display = 'block';
        } else {
            poleDiameterNote.style.display = 'none';
        }
    });

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
            diagramModal.style.display = 'none';
        }
    });
});}