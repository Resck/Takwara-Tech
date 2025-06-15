// docs/assets/js/calculadora.js - Versão com Ajustes Finais para Selects e Dados do Doc

document.addEventListener('DOMContentLoaded', () => {
    const calculatorHTML = `
        <div id="calculator-fixed-box">
            <h2 id="calculator-title">Calculadora de Domos</h2>

            <form id="calculator-form-widget">
                <div class="form-group-widget">
                    <label for="diameter-input-widget">Diâmetro do Domo (m):</label>
                    <input type="number" id="diameter-input-widget" step="0.01" required>
                </div>
                <div class="form-group-widget">
                    <label for="solid-type-input-widget">Sólido Base:</label>
                    <select id="solid-type-input-widget">
                        <option value="Icosahedron">Icosaedro</option>
                        <option value="Cube">Cubo</option>
                        <option value="Octahedron">Octaedro</option>
                        <option value="Dodecahedron">Dodecaedro</option>
                        <option value="Tetrahedron">Tetraedro</option>
                    </select>
                </div>
                <div class="form-group-widget">
                    <label for="frequency-input-widget">Frequência/Variante:</label>
                    <select id="frequency-input-widget" required>
                        <option value="">Selecione a Frequência/Variante</option>
                    </select>
                </div>
                <div class="form-group-widget">
                    <label for="truncation-input-widget">Tipo de Esfera (Truncagem):</label>
                    <select id="truncation-input-widget" required>
                        <option value="">Selecione a Truncagem</option>
                    </select>
                </div>
                <div class="form-group-widget">
                    <label for="connector-measure-input-widget">Medida do Conector (m):</label>
                    <input type="number" id="connector-measure-input-widget" step="0.001" value="0.04" required>
                </div>
                <div class="form-group-widget">
                    <label for="rod-diameter-input-widget">Diâmetro da Vara (cm):</label>
                    <input type="number" id="rod-diameter-input-widget" step="1" required>
                </div>
                <button type="submit">Calcular</button>
            </form>
            <div id="results-container-widget" style="display: none; margin-top: 1rem;">
                <h3>Resultados:</h3>
                <div id="results-table-widget"></div>
                <div id="additional-info-widget"></div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', calculatorHTML);

    const calculatorCSS = `
        #calculator-fixed-box {
            position: fixed; bottom: 20px; right: 20px; background-color: white;
            border: 1px solid #ccc; border-radius: 8px; padding: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15); width: 320px; z-index: 1000;
            font-size: 14px;
        }
        .form-group-widget { margin-bottom: 10px; }
        .form-group-widget label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group-widget input, .form-group-widget select {
            width: calc(100% - 12px); padding: 5px; border: 1px solid #ddd; border-radius: 4px;
        }
        #calculator-form-widget button {
            width: 100%; padding: 8px; background-color: #4CAF50; color: white;
            border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px;
        }
        #calculator-form-widget button:hover { background-color: #45a049; }
        #results-table-widget table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        #results-table-widget th, #results-table-widget td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        #results-table-widget th { background-color: #f2f2f2; }
        #additional-info-widget ul { list-style-type: none; padding: 0; }
        #additional-info-widget li { margin-bottom: 5px; }
        .error-message { color: red; margin-top: 10px; }
    `;
    const styleSheet = document.createElement("style");
    styleSheet.innerText = calculatorCSS;
    document.head.appendChild(styleSheet);

    // --- LÓGICA E INTERATIVIDADE ---
    const calculatorForm = document.getElementById('calculator-form-widget');
    const diameterInput = document.getElementById('diameter-input-widget');
    const solidTypeInput = document.getElementById('solid-type-input-widget');
    const frequencyInput = document.getElementById('frequency-input-widget');
    const truncationInput = document.getElementById('truncation-input-widget');
    const connectorMeasureInput = document.getElementById('connector-measure-input-widget');
    const rodDiameterInput = document.getElementById('rod-diameter-input-widget');
    const resultsContainer = document.getElementById('results-container-widget');
    const resultsTableDiv = document.getElementById('results-table-widget');
    const additionalInfoDiv = document.getElementById('additional-info-widget');

    // Mapeamento dos dados do DOME_DATA para preenchimento dinâmico
    // As chaves e valores devem corresponder exatamente ao DOME_DATA no seu main.py
    const DOME_STRUCTURE_FOR_SELECTS = {
        "Icosahedron": {
            "V1": ["2/3"],
            "V2": ["1/2"],
            "V3": ["3/8", "5/8"],
            "V4": ["1/2"],
            "L3": ["1/2"],
            "V5": ["7/15", "8/15"],
            "V6": ["1/2"],
            "2V.3V": ["1/2"]
        },
        "Cube": {
            "V1": ["N/D"], "V2": ["N/D"], "V3": ["N/D"], "V4": ["N/D"],
            "V5": ["~1/2"],
            "V6": ["1/2"], "2V.3V": ["1/2"], "3V.2V": ["1/2"]
        },
        "Octahedron": {
            "V1": ["1/2"], "V2": ["1/2"], "V3": ["1/2"],
            "L3_3/8": ["3/8"], "L3_5/8": ["5/8"],
            "V4": ["N/D"], "V5": ["N/D"], "V6": ["N/D"]
        },
        "Dodecahedron": {
            "L1": ["N/D"], "L2": ["N/D"], "L2T": ["N/D"]
        },
        "Tetrahedron": {
            "L2T": ["N/D"], "L3T": ["N/D"]
        }
    };


    // Função para popular as opções de frequência e truncagem
    function populateFrequenciesAndTruncations() {
        const selectedSolid = solidTypeInput.value;
        const frequencies = DOME_STRUCTURE_FOR_SELECTS[selectedSolid] || {};

        // Limpa e popula as frequências
        frequencyInput.innerHTML = '<option value="">Selecione a Frequência/Variante</option>';
        for (const freqKey in frequencies) {
            const option = document.createElement('option');
            option.value = freqKey; // O VALOR do option é a chave exata para o backend (ex: "V3", "L3")
            option.textContent = freqKey;
            frequencyInput.appendChild(option);
        }

        // Limpa a truncagem e a desabilita até que uma frequência seja selecionada
        truncationInput.innerHTML = '<option value="">Selecione a Truncagem</option>';
        truncationInput.disabled = true; // Desabilita o select de truncagem

        // Adiciona/Atualiza o listener para mudança de frequência
        // Remova listeners anteriores para evitar duplicação
        frequencyInput.removeEventListener('change', handleFrequencyChange);
        frequencyInput.addEventListener('change', handleFrequencyChange);
    }

    function handleFrequencyChange() {
        const selectedSolid = solidTypeInput.value;
        const selectedFrequency = frequencyInput.value;
        const truncations = DOME_STRUCTURE_FOR_SELECTS[selectedSolid]?.[selectedFrequency] || [];

        truncationInput.innerHTML = '<option value="">Selecione a Truncagem</option>';
        if (truncations.length > 0) {
            truncations.forEach(trunc => {
                const option = document.createElement('option');
                option.value = trunc; // O VALOR do option é a chave exata para o backend (ex: "3/8", "N/D")
                option.textContent = trunc;
                truncationInput.appendChild(option);
            });
            truncationInput.disabled = false; // Habilita o select de truncagem
        } else {
            truncationInput.disabled = true; // Mantém desabilitado se não houver truncagens
        }
    }


    // Popula inicialmente ao carregar a página
    populateFrequenciesAndTruncations();
    solidTypeInput.addEventListener('change', populateFrequenciesAndTruncations);


    // ATENÇÃO: Verifique se este URL está correto para sua Cloud Function implantada!
    const apiUrl = 'https://us-central1-adroit-citadel-397215.cloudfunctions.net/calculadora-domo-api';

    calculatorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        resultsTableDiv.innerHTML = '';
        additionalInfoDiv.innerHTML = '';
        resultsContainer.style.display = 'none'; // Esconde resultados enquanto calcula

        // Validação básica para garantir que todos os selects foram preenchidos
        if (!diameterInput.value || !solidTypeInput.value || !frequencyInput.value ||
            !truncationInput.value || !connectorMeasureInput.value || !rodDiameterInput.value) {
            resultsTableDiv.innerHTML = `<p class="error-message">Por favor, preencha todos os campos da calculadora.</p>`;
            resultsContainer.style.display = 'block';
            return; // Interrompe o envio se algum campo estiver vazio
        }


        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    diameter: diameterInput.value,
                    frequency: frequencyInput.value, // Envia a chave formatada (ex: "V3", "L3")
                    truncation: truncationInput.value, // Envia a chave formatada (ex: "3/8", "N/D")
                    solid_type: solidTypeInput.value,
                    connector_measure: connectorMeasureInput.value,
                    rod_diameter: rodDiameterInput.value
                }),
            });
            const data = await response.json();

            if (data.success) {
                displayResults(data);
                resultsContainer.style.display = 'block';
            } else {
                resultsTableDiv.innerHTML = `<p class="error-message">Erro da API: ${data.error}</p>`;
                resultsContainer.style.display = 'block';
            }
        } catch (error) {
            resultsTableDiv.innerHTML = `<p class="error-message">Erro ao conectar à API: ${error.message}. Verifique a URL da API ou o console para mais detalhes.</p>`;
            console.error("Erro na requisição da API:", error);
            resultsContainer.style.display = 'block';
        }
    });

    function displayResults(data) {
        // Tabela de Segmentos
        let tableHTML = '<table><thead><tr><th>Tipo</th><th>Comp. Normal (m)</th><th>Val. Conector (-) (m)</th><th>Comp. Final (m)</th><th>Qtd.</th><th>Ângulo (graus)</th></tr></thead><tbody>';
        // Verificar se segment_data é um objeto e tem chaves antes de iterar
        if (data.segment_data && typeof data.segment_data === 'object' && Object.keys(data.segment_data).length > 0) {
            for (const type in data.segment_data) {
                const segment = data.segment_data[type];
                tableHTML += `<tr>
                    <td>${type}</td>
                    <td>${segment.normal_length}</td>
                    <td>${segment.connector_deduction}</td>
                    <td>${segment.final_length}</td>
                    <td>${segment.quantity}</td>
                    <td>${segment.angle}</td>
                </tr>`;
            }
        } else {
            tableHTML += `<tr><td colspan="6">Dados de segmentos não disponíveis para esta seleção.</td></tr>`;
        }
        tableHTML += '</tbody></table>';
        resultsTableDiv.innerHTML = tableHTML;

        // Informações Adicionais
        let additionalHTML = '<h3>Informações de Produção:</h3><ul>';
        additionalHTML += `<li>Diâmetro das Conexões (Total): ${data.connection_diameter} m</li>`;
        additionalHTML += `<li>Número Total de Conectores (Sapatilhas): ${data.total_connectors}</li>`;
        additionalHTML += `<li>Cabo de Aço: ${data.cable_info}</li>`;
        additionalHTML += `<li>Consumo de PU Vegetal: ${data.total_pu_veg}</li>`;
        additionalHTML += `<li>Consumo de PU Expansivo: ${data.total_pu_exp}</li>`;
        additionalHTML += '</ul>';
        additionalInfoDiv.innerHTML = additionalHTML;
    }
});