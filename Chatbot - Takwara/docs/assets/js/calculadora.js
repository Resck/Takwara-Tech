// docs/assets/js/calculadora.js - VERSÃO COM EXPORTAÇÃO CSV

document.addEventListener('DOMContentLoaded', () => {
    // A base de dados que o seu backend usa. Vamos espelhá-la aqui
    // para que o frontend possa criar os menus dinamicamente.
    const DOME_DATA = {
        "Icosahedron": {
            "V1": {"truncation": ["2/3"]},
            "V2": {"truncation": ["1/2"]},
            "V3": {"truncation": ["3/8", "5/8"]},
            "V4": {"truncation": ["1/2"]},
            "L3": {"truncation": ["1/2"]},
            "V5": {"truncation": ["7/15", "8/15"]},
            "V6": {"truncation": ["1/2"]},
            "2V.3V": {"truncation": ["1/2"]}
        },
        "Cube": {
            "V1": {"truncation": ["N/D"]},
            "V2": {"truncation": ["N/D"]},
            "V3": {"truncation": ["N/D"]},
            "V4": {"truncation": ["N/D"]},
            "V5": {"truncation": ["~1/2"]},
            "V6": {"truncation": ["1/2"]},
            "2V.3V": {"truncation": ["1/2"]},
            "3V.2V": {"truncation": ["1/2"]}
        },
        "Octahedron": {
            "V1": {"truncation": ["1/2"]},
            "V2": {"truncation": ["1/2"]},
            "V3": {"truncation": ["1/2"]},
            "L3_3/8": {"truncation": ["3/8"]},
            "L3_5/8": {"truncation": ["5/8"]},
            "V4": {"truncation": ["N/D"]},
            "V5": {"truncation": ["N/D"]},
            "V6": {"truncation": ["N/D"]}
        },
        "Dodecahedron": {
            "L1": {"truncation": ["N/D"]},
            "L2": {"truncation": ["N/D"]},
            "L2T": {"truncation": ["N/D"]}
        },
        "Tetrahedron": {
            "L2T": {"truncation": ["N/D"]},
            "L3T": {"truncation": ["N/D"]}
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
                <button type="submit">Calcular</button>
            </form>
            <div id="results-container-widget" style="display: none; margin-top: 1rem;">
                <h4>Resultados:</h4>
                <div id="results-table-widget"></div>
                <div id="export-button-container-widget"></div>
            </div>
            <p id="error-message-widget" style="color: red;"></p>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', calculatorHTML);

    // --- 2. ADICIONAR ESTILOS CSS ---
    const calculatorCSS = `#calculator-fixed-box{position:fixed;bottom:20px;right:20px;background-color:#fff;border:1px solid #ccc;border-radius:8px;padding:15px;box-shadow:0 4px 8px rgba(0,0,0,0.15);width:300px;z-index:1000;font-size:14px;} #calculator-fixed-box h2{font-size:1.1rem; margin-top:0; text-align:center;} .form-group-widget{margin-bottom:10px;} .form-group-widget label{display:block;margin-bottom:5px;font-weight:bold;} .form-group-widget input, .form-group-widget select{width:100%;padding:8px;box-sizing:border-box;} #results-container-widget h4{margin-top:15px;margin-bottom:10px;border-top:1px solid #eee;padding-top:10px;} #results-container-widget table{width:100%;border-collapse:collapse;font-size:13px;} #results-container-widget th, #results-container-widget td{border:1px solid #ddd;padding:5px;text-align:left;} #export-csv-button-widget{margin-top:10px; padding: 8px 12px; cursor: pointer;}`;
    const styleSheet = document.createElement("style");
    styleSheet.innerText = calculatorCSS;
    document.head.appendChild(styleSheet);

    // --- 3. LÓGICA E INTERATIVIDADE ---
    const calculatorForm = document.getElementById('calculator-form-widget');
    const solidSelect = document.getElementById('base-solid-input-widget');
    const freqSelect = document.getElementById('frequency-input-widget');
    const truncSelect = document.getElementById('truncation-input-widget');
    const resultsContainer = document.getElementById('results-container-widget');
    const resultsTableDiv = document.getElementById('results-table-widget');
    const errorMessageP = document.getElementById('error-message-widget');
    // --- NOVO --- Referência para o contentor do botão
    const exportButtonContainer = document.getElementById('export-button-container-widget');

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
        const truncs = DOME_DATA[selectedSolid]?.[selectedFreq]?.truncation || [];
        populateSelect(truncSelect, truncs);
    }

    // Event Listeners para menus dinâmicos
    solidSelect.addEventListener('change', updateFreqOptions);
    freqSelect.addEventListener('change', updateTruncOptions);

    // Lógica de submissão do formulário
    calculatorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        resultsContainer.style.display = 'none';
        errorMessageP.textContent = '';
        exportButtonContainer.innerHTML = ''; // --- NOVO --- Limpa o botão antigo
        
        const payload = {
            diameter: document.getElementById('diameter-input-widget').value,
            base_solid: solidSelect.value,
            frequency: freqSelect.value,
            truncation: truncSelect.value
        };

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            const data = await response.json();
            if (data.success) {
                displayResults(data);
            } else {
                errorMessageP.textContent = data.error || 'Ocorreu um erro.';
            }
        } catch (error) {
            errorMessageP.textContent = 'Erro de comunicação com a API.';
        }
        resultsContainer.style.display = 'block';
    });

    // --- ALTERADO --- Função para mostrar os resultados
    function displayResults(data) {
        let tableHTML = '<table><thead><tr><th>Tipo</th><th>Comp. (m)</th><th>Qtd.</th></tr></thead><tbody>';
        for (const key in data.segment_lengths) {
            tableHTML += `<tr><td>${key}</td><td>${data.segment_lengths[key]}</td><td>${data.num_segments[key]}</td></tr>`;
        }
        tableHTML += '</tbody></table>';
        resultsTableDiv.innerHTML = tableHTML;
        
        // --- NOVO --- Cria e adiciona o botão de exportação dinamicamente
        const exportButtonHTML = `<button id="export-csv-button-widget">Exportar para CSV</button>`;
        exportButtonContainer.innerHTML = exportButtonHTML;

        // --- NOVO --- Adiciona o "ouvinte" de evento ao novo botão
        document.getElementById('export-csv-button-widget').addEventListener('click', () => {
            exportToCSV(data);
        });
    }

    // --- NOVO --- Função para formatar os dados e descarregar o ficheiro CSV
    function exportToCSV(data) {
        // 1. Cria o cabeçalho do CSV
        let csvContent = "Tipo,Comprimento (m),Quantidade\n";

        // 2. Adiciona uma linha para cada tipo de vara
        for (const key in data.segment_lengths) {
            const length = data.segment_lengths[key];
            const quantity = data.num_segments[key];
            csvContent += `${key},${length},${quantity}\n`;
        }

        // 3. Cria um "blob" (um objeto de ficheiro) com o conteúdo
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });

        // 4. Cria um link temporário para iniciar o download
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", "calculo_domo_takwara.csv");
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        
        // 5. Simula um clique no link para descarregar e depois remove-o
        link.click();
        document.body.removeChild(link);
    }


    // Inicializa o formulário
    populateSelect(solidSelect, Object.keys(DOME_DATA));
    updateFreqOptions();
});