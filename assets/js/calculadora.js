// docs/assets/js/calculadora.js - OTIMIZADA PARA TOOLBOX E SHADOW DOM

document.addEventListener('takwara:tools-ready', (event) => {
    const shadowRoot = event.detail.shadowRoot;
    initializeTakwaraCalculator(shadowRoot);
});

function initializeTakwaraCalculator(shadowRoot) {
    console.log('Takwara Calculadora: A inicializar após receber o sinal "tools-ready".');

    // A base de dados que o seu backend usa para popular os menus dinamicamente.
    const DOME_DATA = { /* ... (conteúdo original da sua DOME_DATA) ... */ };
    const DOME_IMAGES = { /* ... (conteúdo original da sua DOME_IMAGES) ... */ };

    // --- 1. LÓGICA E INTERATIVIDADE ---
    // Agora todos os elementos são obtidos via shadowRoot.getElementById
    const calculatorForm = shadowRoot.getElementById('calculator-form-widget');
    const solidSelect = shadowRoot.getElementById('base-solid-input-widget');
    const freqSelect = shadowRoot.getElementById('frequency-input-widget');
    const truncSelect = shadowRoot.getElementById('truncation-input-widget');
    const poleDiameterInput = shadowRoot.getElementById('pole-diameter-input-widget');
    const resultsContainer = shadowRoot.getElementById('results-container-widget');
    const resultsTableDiv = shadowRoot.getElementById('results-table-widget');
    const materialCostsDiv = shadowRoot.getElementById('material-costs-widget');
    const errorMessageP = shadowRoot.getElementById('error-message-widget');
    const diagramSection = shadowRoot.getElementById('diagram-section-widget');
    const domeDiagramImg = shadowRoot.getElementById('dome-diagram-img');
    const viewDiagramButton = shadowRoot.getElementById('view-diagram-button');
    const diagramModal = shadowRoot.getElementById('diagram-modal');
    const modalDiagramImg = shadowRoot.getElementById('modal-diagram-img');
    const closeDiagramModal = shadowRoot.getElementById('close-diagram-modal');
    const poleDiameterNote = shadowRoot.getElementById('pole-diameter-note');
    const downloadResultsButton = shadowRoot.getElementById('download-results-button');
    const footerNotes = shadowRoot.getElementById('footer-notes');

    if (!calculatorForm || !solidSelect || !freqSelect || !truncSelect) {
        console.error('Takwara Calculadora: Um ou mais elementos HTML essenciais não foram encontrados no Shadow DOM. Verifique o HTML no template `widget-calculadora.html`.');
        return;
    }

    let lastCalculatedData = null;
    let lastSelectedSolid = '';
    let lastSelectedFreq = '';
    let lastSelectedTrunc = '';
    let lastPoleDiameterCm = 'N/A';
    let lastTotalLinearMeters = 0;

    const apiUrl = 'https://southamerica-east1-adroit-citadel-397215.cloudfunctions.net/calculadora-domo-api';

    function populateSelect(selectElement, options) {
        selectElement.innerHTML = '';
        if (options.length === 0) {
            const opt = shadowRoot.createElement('option'); // Cria elemento no Shadow DOM
            opt.value = "";
            opt.textContent = "N/D";
            selectElement.appendChild(opt);
            selectElement.disabled = true;
        } else {
            selectElement.disabled = false;
            options.forEach(option => {
                const opt = shadowRoot.createElement('option'); // Cria elemento no Shadow DOM
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

        if (imageUrl && domeDiagramImg) {
            domeDiagramImg.src = imageUrl;
            diagramSection.style.display = 'block';
        } else if (diagramSection) {
            diagramSection.style.display = 'none';
            if (domeDiagramImg) domeDiagramImg.src = '';
        }
    }

    function customRound(value) {
        if (typeof value !== 'number' || isNaN(value)) {
            return 'N/A';
        }
        return (Math.round(value * 100) / 100).toFixed(2);
    }

    calculatorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (resultsContainer) resultsContainer.style.display = 'none';
        if (errorMessageP) errorMessageP.textContent = '';
        if (materialCostsDiv) materialCostsDiv.innerHTML = '';
        if (diagramSection) diagramSection.style.display = 'none';
        if (downloadResultsButton) downloadResultsButton.style.display = 'none';
        if (footerNotes) footerNotes.style.display = 'none';

        const diameter = parseFloat(shadowRoot.getElementById('diameter-input-widget').value); // Acessa via shadowRoot
        const base_solid = solidSelect.value;
        const frequency = freqSelect.value;
        const truncation = truncSelect.value;

        let poleDiameterCm = parseFloat(poleDiameterInput.value);
        
        if (isNaN(parseFloat(poleDiameterInput.value)) || parseFloat(poleDiameterInput.value) <= 0) {
            poleDiameterCm = "N/A";
            if (poleDiameterNote) poleDiameterNote.style.display = 'block';
        } else {
            if (poleDiameterNote) poleDiameterNote.style.display = 'none';
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
                const SPACING_MM = 4;
                const SPACING_CM = SPACING_MM / 10;
                let connectorCutoffValueCm = 0;
                let actualConnectorCutoffMeters = 0;

                if (typeof poleDiameterCm === 'number' && poleDiameterCm > 0) {
                    const calculatedVertexDiameter = 2 * (1.5 * poleDiameterCm + SPACING_CM);
                    connectorCutoffValueCm = (calculatedVertexDiameter / 2);
                    actualConnectorCutoffMeters = (2 * connectorCutoffValueCm / 100);
                }
                
                let totalLinearMetersCalculated = 0;
                let totalSegmentsCalculated = 0;
                let segmentResultsForDisplay = [];

                for (const key in data.segment_lengths) {
                    const originalLength = parseFloat(data.segment_lengths[key]);
                    const quantity = data.num_segments[key];
                    const vertexAngle = data.vertex_angles[key];

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
                
                lastTotalLinearMeters = totalLinearMetersCalculated;
                lastCalculatedData = { ...data, segmentResultsForDisplay: segmentResultsForDisplay };

                displayResults(data, diameter, poleDiameterCm, totalLinearMetersCalculated, totalSegmentsCalculated, segmentResultsForDisplay);
                updateDiagramImage();
                if (downloadResultsButton) downloadResultsButton.style.display = 'block';

                lastSelectedSolid = base_solid;
                lastSelectedFreq = frequency;
                lastSelectedTrunc = truncation;
                lastPoleDiameterCm = poleDiameterCm;

            } else {
                if (errorMessageP) errorMessageP.textContent = data.error || 'Ocorreu um erro.';
            }
        } catch (error) {
            if (errorMessageP) errorMessageP.textContent = 'Erro de comunicação com a API: ' + error.message;
        }
        if (resultsContainer) resultsContainer.style.display = 'block';
    });

    function displayResults(data, domeDiameter, poleDiameterCm, totalLinearMeters, totalSegments, segmentResultsForDisplay) {
        let tableHTML = '<table><thead><tr><th>Tipo</th><th>Comp. Original (m)</th><th>Desconto Conector (m)</th><th>Comp. Final (m)</th><th>Qtd.</th><th>Ângulo (\u03B1)</th></tr></thead><tbody>';
        
        segmentResultsForDisplay.forEach(segment => {
            const originalLengthRounded = customRound(segment.originalLength);
            const discountRounded = customRound(segment.discount);
            const finalLengthRounded = customRound(segment.finalLength); 

            tableHTML += `<tr><td>${segment.type}</td><td>${originalLengthRounded}</td><td>${discountRounded}</td><td>${finalLengthRounded}</td><td>${segment.quantity}</td><td>${segment.angle !== 'N/D' ? segment.angle.toFixed(2) + '\u00B0' : 'N/A'}</td></tr>`;
        });

        tableHTML += '</tbody></table>';
        if (resultsTableDiv) resultsTableDiv.innerHTML = tableHTML;

        let materialHTML = '<h4>Recursos Materiais:</h4><ul>';

        const numVertices = typeof data.total_vertices === 'number' ? data.total_vertices : 'N/A'; 

        materialHTML += `<li>Número de Vértices: ${numVertices}</li>`;
        materialHTML += `<li>Número Total de Varas: ${totalSegments}</li>`;
        materialHTML += `<li>Total de Metros Lineares de Varas de Bambu: ${totalLinearMeters.toFixed(2)} m</li>`;
        
        const numConectores = totalSegments * 2;
        materialHTML += `<li>Número de Conectores Utilizados: ${numConectores} (2 por vara)</li>`;

        let cableLengthPerRod = 2;
        if (typeof poleDiameterCm === 'number' && poleDiameterCm >= 6.5) {
            cableLengthPerRod = 3;
        }
        const totalCableLength = totalSegments * cableLengthPerRod;

        materialHTML += `<li>Cabo de Aço: ${totalCableLength} m</li>`;
        materialHTML += `<li>Número de Sapatilhas: ${totalSegments * 2}</li>`;
        materialHTML += `<li>Prensa Cabo: ${totalSegments * 4}</li>`;
        materialHTML += `<li>Arruelas: ${totalSegments * 4}</li>`;
        materialHTML += `<li>Parafusos com Porcas: ${numConectores}</li>`;

        let puUg132aMl = 0;
        if (typeof poleDiameterCm === 'number') {
            if (poleDiameterCm > 0 && poleDiameterCm <= 5) {
                puUg132aMl = 30 * totalLinearMeters;
            } else if (poleDiameterCm > 5 && poleDiameterCm <= 10) {
                puUg132aMl = 60 * totalLinearMeters;
            }
        }
        const displayPuUg132a = puUg132aMl >= 1000 ? `${(puUg132aMl / 1000).toFixed(2)} L` : `${puUg132aMl.toFixed(2)} ml`;
        materialHTML += `<li>PU Vegetal UG132A: ${typeof puUg132aMl === 'number' && puUg132aMl > 0 ? displayPuUg132a : 'N/A'}</li>`;

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

        let vertexDiameterDisplay = 'N/A';
        let connectorLengthCm = 'N/A';
        const SPACING_MM = 4;
        const SPACING_CM = SPACING_MM / 10;

        if (typeof poleDiameterCm === 'number' && poleDiameterCm > 0) {
            const calculatedVertexDiameter = 2 * (1.5 * poleDiameterCm + SPACING_CM);
            vertexDiameterDisplay = calculatedVertexDiameter.toFixed(2) + ' cm';
            connectorLengthCm = (calculatedVertexDiameter / 2).toFixed(2);
        }
        materialHTML += `<li>Diâmetro dos Vértices (estimado): ${vertexDiameterDisplay}</li>`;

        materialHTML += `<li>Número de Anéis de Borracha: ${typeof numVertices === 'number' ? numVertices : 'N/A'}</li>`;
        materialHTML += `</ul>`;
        if (materialCostsDiv) materialCostsDiv.innerHTML = materialHTML;

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
        if (footerNotes) {
            footerNotes.innerHTML = notesHTML;
            footerNotes.style.display = 'block';
        }
    }

    function generateMarkdown() {
        const diameter = shadowRoot.getElementById('diameter-input-widget').value; // Acessa via shadowRoot
        const base_solid = lastSelectedSolid;
        const frequency = lastSelectedFreq;
        const truncation = lastSelectedTrunc;
        const poleDiameterCm = lastPoleDiameterCm;
        const data = lastCalculatedData;
        const totalLinearMetersMd = lastTotalLinearMeters;
        const totalSegmentsMd = data.total_segments;

        const diagramImageUrl = domeDiagramImg ? domeDiagramImg.src : '';

        let markdownContent = `# Resultados da Calculadora de Domos\n\n`;
        markdownContent += `## Detalhes do Domo\n`;
        markdownContent += `- **Sólido Base:** ${base_solid}\n`;
        markdownContent += `- **Frequência/Variante:** ${frequency}\n`;
        markdownContent += `- **Tipo de Esfera (Truncagem):** ${truncation}\n`;
        markdownContent += `- **Diâmetro do Domo:** ${diameter} m\n`;
        markdownContent += `- **Diâmetro das Varas:** ${typeof poleDiameterCm === 'number' ? poleDiameterCm + ' cm' : 'N/A (Cálculo de PU e Cabo de Aço pode ser afetado)'}\n`;
        markdownContent += `\n`;

        markdownContent += `## Comprimento dos Segmentos\n\n`;
        markdownContent += `| Tipo | Comp. Original (m) | Desconto Conector (m) | Comp. Final (m) | Qtd. | Ângulo (α) |\n`;
        markdownContent += `|---|---|---|---|---|---|\n`;
        lastCalculatedData.segmentResultsForDisplay.forEach(segment => {
            markdownContent += `| ${segment.type} | ${customRound(segment.originalLength)} | ${customRound(segment.discount)} | ${customRound(segment.finalLength)} | ${segment.quantity} | ${segment.angle !== 'N/D' ? segment.angle.toFixed(2) + '°' : 'N/A'} |\n`;
        });
        markdownContent += `\n`;

        markdownContent += `## Recursos Materiais\n\n`;

        const numVerticesMd = typeof data.total_vertices === 'number' ? data.total_vertices : 'N/A';

        markdownContent += `- Número de Vértices: ${numVerticesMd}\n`;
        markdownContent += `- Número Total de Varas: ${totalSegmentsMd}\n`;
        markdownContent += `- Número Total de Metros Lineares de Varas de Bambu: ${typeof totalLinearMetersMd === 'number' ? totalLinearMetersMd.toFixed(2) : 'N/A'} m\n`;      
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

    if (downloadResultsButton) {
        downloadResultsButton.addEventListener('click', () => {
            if (!lastCalculatedData) {
                if (errorMessageP) errorMessageP.textContent = 'Por favor, execute um cálculo antes de baixar os resultados.';
                return;
            }
            const markdown = generateMarkdown();
            const filename = `resultados_domo_${lastSelectedSolid.replace(/\s/g, '_')}_${lastSelectedFreq.replace(/\//g, '-')}_${lastSelectedTrunc.replace(/\//g, '-')}.md`;
            const blob = new Blob([markdown], { type: 'text/markdown;charset=utf-8;' });
            const link = shadowRoot.createElement('a'); // Cria elemento no Shadow DOM
            if (link.download !== undefined) {
                link.setAttribute('href', URL.createObjectURL(blob));
                link.setAttribute('download', filename);
                link.style.visibility = 'hidden';
                shadowRoot.appendChild(link); // Anexa ao Shadow DOM
                link.click();
                link.remove(); // Remove do Shadow DOM
            } else {
                alert('Seu navegador não suporta o download automático. Copie o texto abaixo:\n\n' + markdown);
            }
        });
    }

    populateSelect(solidSelect, Object.keys(DOME_DATA));
    solidSelect.addEventListener('change', updateFreqOptions);
    freqSelect.addEventListener('change', updateTruncOptions);
    truncSelect.addEventListener('change', updateDiagramImage);

    updateFreqOptions();

    if (poleDiameterInput && poleDiameterNote) {
        poleDiameterInput.addEventListener('input', () => {
            if (isNaN(parseFloat(poleDiameterInput.value)) || parseFloat(poleDiameterInput.value) <= 0) {
                poleDiameterNote.style.display = 'block';
            } else {
                poleDiameterNote.style.display = 'none';
            }
        });
    }

    if (viewDiagramButton && modalDiagramImg && diagramModal && closeDiagramModal) {
        viewDiagramButton.addEventListener('click', () => {
            modalDiagramImg.src = domeDiagramImg.src;
            diagramModal.style.display = 'block';
        });

        closeDiagramModal.addEventListener('click', () => {
            diagramModal.style.display = 'none';
        });

        // Este listener ainda pode ser no window, pois o modal está no documento principal
        window.addEventListener('click', (event) => {
            if (event.target == diagramModal) {
                diagramModal.style.display = 'none';
            }
        });
    }
}