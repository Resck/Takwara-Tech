# Calculadora de Domos Geodésicos - Tecnologia Takwara

Este repositório hospeda a Calculadora de Domos Geodésicos do projeto Tecnologia Takwara, uma ferramenta interativa projetada para auxiliar arquitetos, engenheiros, estudantes e pesquisadores no planejamento e dimensionamento de domos geodésicos em bambu. A calculadora fornece estimativas precisas para comprimentos de segmentos, quantidades de materiais e outros parâmetros cruciais para a construção dessas estruturas inovadoras.

## Função e Importância

A calculadora serve como uma ferramenta fundamental para diversos trabalhos de pesquisa e aplicação prática, permitindo:

* **Validação de Projetos:** Testar rapidamente diferentes configurações de domos (sólido base, frequência e truncagem) e visualizar seus impactos nos comprimentos e materiais.
* **Otimização de Recursos:** Obter estimativas detalhadas de varas de bambu, conectores, cabos de aço, parafusos, anéis de borracha e selantes (PU Vegetal), auxiliando na orçamentação e na gestão de materiais.
* **Apoio à Pesquisa:** Servir como um recurso valioso para estudos sobre a geometria e a viabilidade construtiva de domos geodésicos em bambu, facilitando a comparação entre diferentes tipologias.
* **Método Educacional:** Proporcionar uma compreensão prática das relações geométricas e materiais envolvidas na construção de domos geodésicos.

## Tecnologia por Trás

A Calculadora de Domos Geodésicos é uma aplicação web interativa desenvolvida com as seguintes tecnologias:

* **Frontend (HTML, CSS, JavaScript):** A interface do usuário é construída dinamicamente usando JavaScript e estilizada com CSS, garantindo uma experiência responsiva e intuitiva. O JavaScript também gerencia a lógica de interação dos formulários e a exibição dos resultados.
* **Backend (Python com Google Cloud Functions):** Os cálculos complexos de comprimentos de segmentos e ângulos são realizados por uma API RESTful desenvolvida em Python, hospedada no Google Cloud Functions. Esta arquitetura serverless garante escalabilidade, baixo custo e alta disponibilidade.
* **GitHub Pages:** O portal "Tecnologia Takwara" e a calculadora são hospedados no GitHub Pages, um serviço gratuito que permite a publicação de sites estáticos diretamente de um repositório GitHub.

## Coleta de Dados para o Funcionamento

O funcionamento da calculadora baseia-se em uma base de dados estruturada que armazena os coeficientes geométricos e informações de vértices para diversas configurações de domos. Esses dados são coletados de fontes confiáveis e literatura especializada em geometria geodésica. A base de dados (`DOME_DATA`) contém informações sobre:

* **Sólidos Base:** Icosaedro, Cubo, Octaedro, Dodecaedro, Tetraedro.
* **Frequências/Variantes:** Diferentes níveis de subdivisão da cúpula (V1, V2, V3, L3, etc.).
* **Tipos de Esfera (Truncagens):** Variantes da forma da cúpula (ex: 2/3, 1/2, 3/8, 5/8), que afetam a distribuição dos segmentos e o número de vértices.

Os coeficientes fornecidos por essa base de dados são multiplicados pelo raio do domo desejado para obter os comprimentos reais dos segmentos.

## Passos para Implantação no GitHub Pages

Para implantar esta calculadora no seu próprio GitHub Pages, siga os passos abaixo:

1.  **Estrutura do Repositório:** Certifique-se de que seus arquivos estejam organizados de forma semelhante à seguinte estrutura (ou ajuste os caminhos no seu código):
    ```
    seu-repositorio/
    ├── docs/
    │   ├── assets/
    │   │   ├── css/
    │   │   ├── js/
    │   │   │   └── calculadora.js  (Este arquivo)
    │   │   └── images/
    │   │       └── domes/
    │   │           └── ... (Imagens dos diagramas)
    │   └── index.md (Ou outros arquivos Markdown do seu site)
    ├── backend-api/
    │   ├── main.py  (O código da sua Cloud Function)
    │   └── requirements.txt (Dependências do Python para a Cloud Function)
    └── .github/
        └── workflows/
            └── deploy.yml (Opcional, para automação do GitHub Actions)
    ```
2.  **Configuração da Cloud Function (Backend):**
    * No Google Cloud Console, crie uma nova função Cloud Functions (Gen 2, se possível).
    * Defina o nome da função (ex: `calculadora-domo-api`).
    * Selecione o runtime `Python 3.9` (ou compatível).
    * Defina o `Entry point` como `calculadora_domo_api`.
    * No código-fonte, selecione o diretório que contém seu `main.py` e `requirements.txt` (ex: `backend-api/`).
    * Certifique-se de que seu `requirements.txt` contenha apenas as dependências mínimas para a calculadora (`functions-framework`, `Flask`).
    * Configure o trigger como `HTTP`.
    * Permita invocações não autenticadas (`Allow unauthenticated invocations`).
    * Implante a função. Anote a URL gerada, você precisará dela no frontend.
    * **Importante:** Garanta que a `DOME_DATA` no seu `main.py` backend esteja com os valores de `total_vertices` como números (não "N/D") para as combinações onde eles existem.

3.  **Atualização do Frontend (JavaScript):**
    * Abra o arquivo `docs/assets/js/calculadora.js`.
    * Localize a linha `const apiUrl = 'SUA_URL_DA_API';`.
    * Substitua `'SUA_URL_DA_API'` pela URL da sua Cloud Function que você anotou no passo anterior.
    * Salve o arquivo.

4.  **Habilitar GitHub Pages:**
    * No seu repositório GitHub, vá em `Settings` > `Pages`.
    * Em `Source`, selecione a branch `main` (ou `master`) e a pasta `/docs` (se você usa o MkDocs ou arquivos diretamente no `/docs`).
    * Salve as alterações. Seu site será construído e estará disponível na URL do GitHub Pages.

5.  **Sincronização:**
    * Faça `git add .`, `git commit -m "Atualiza calculadora e README"`, e `git push origin main` para enviar suas alterações para o GitHub.

## Licença

Este projeto está licenciado sob a [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.pt). Você é livre para:

* **Compartilhar** — copiar e redistribuir o material em qualquer suporte ou formato.
* **Adaptar** — remixar, transformar, e criar a partir do material para quaisquer fins, mesmo que comerciais.

Desde que você dê o devido crédito, forneça um link para a licença e indique se foram feitas alterações. Você pode fazê-lo de qualquer forma razoável, mas não de forma a sugerir que o licenciador o endossa ou o seu uso.

---
# 10/06/2025

Memorial de Ajustes e Falhas da Calculadora de Domos Geodésicos (Versão Atualizada)
Este memorial consolida o histórico de desenvolvimento, as melhorias implementadas, as falhas persistentes e os próximos passos cruciais para a Calculadora de Domos Geodésicos do projeto Tecnologia Takwara. Ele também incorpora diretrizes para o desenvolvimento futuro e a produção de conteúdo original.

Resumo das Melhorias Implementadas e Falhas Atuais:

A calculadora evoluiu significativamente, com a criação de uma interface dinâmica, cálculos de materiais avançados e a funcionalidade de exportação de resultados. No entanto, persistem desafios relacionados à consistência dos dados, à lógica de menus e à exibição de informações fundamentais.

Frontend (docs/assets/js/calculadora.js):

Injeção de HTML e CSS: A calculadora é injetada dinamicamente como um "widget" flutuante.
Menus Dinâmicos: A lógica para popular os dropdowns de "Sólido Base", "Frequência/Variante" e "Tipo de Esfera" foi implementada com base no DOME_DATA. No entanto, uma falha crítica foi observada:
Problema: Opções de Frequência/Truncagem para as quais não há dados completos (ex: Dodecahedron L2T, Cube V1) continuam a aparecer nos menus, levando a erros "Combinação de Sólido/Frequência/Truncagem não encontrada. Chave ausente: 'L2T'." ou a resultados "N/D" inesperados na tabela.
Objetivo: Os menus devem exibir apenas as opções de Frequência e Truncagem para as quais há dados válidos e completos no DOME_DATA do backend (segmentos, quantidades, ângulos e total_vertices). Se uma frequência/truncagem não possuir esses dados, ela não deve ser uma opção selecionável.
Cálculos de Materiais Avançados: Adição de cálculos para número de vértices, total de metros lineares de varas, conectores, sapatilhas, cabo de aço, prensas cabo, arruelas, PU Vegetal (UG132A e Mamonex RD70), diâmetro estimado dos vértices e anéis de borracha.
Unidades de Medida: A conversão de ml para Litros para PU Vegetal acima de 1000ml foi implementada.
Diâmetro dos Vértices (Cálculo e Observação Crítica):
Problema: O cálculo do diâmetro dos vértices era inicialmente impreciso e não refletia a realidade da união de varas. O valor anterior de "34.00 cm" para vara de 5cm era um erro.
Melhoria Implementada: O cálculo foi corrigido para 2 * (1.5 * Diâmetro da Vara (cm) + 0.4 cm), resultando em 15.80 cm para uma vara de 5cm, que é um "parâmetro real de construção" validado. A observação no rodapé e no Markdown foi atualizada para descrever este cálculo (6 varas dispostas circularmente, espaçamento de 4mm) e sua importância.
Próximo Ajuste Crucial: Descontar o valor da conexão do comprimento final da vara. Esta é uma consideração de engenharia estrutural essencial: o comprimento útil da vara é o seu comprimento total menos as porções que são engastadas na conexão. Este valor de desconto (metade do diâmetro do vértice de cada extremidade da vara) deve ser subtraído do comprimento de cada segmento de vara calculado. Isso garantirá que o diâmetro final da estrutura construída corresponda precisamente ao diâmetro de projeto, evitando superdimensionamento pós-conexão. A precisão deste dado realça a importância crítica da entrada do diâmetro do bambu.
Entradas no Formulário: O campo "Desconto Conector" foi removido do formulário, pois seu valor será derivado do diâmetro dos vértices.
Exibição de Diagramas e Modal: Funcionalidade para exibir diagramas e um modal para visualização ampliada foram adicionadas.
Diretriz para Imagens: As imagens dos diagramas de montagem e das tipologias de domos devem ser geradas internamente pela equipe de assistentes. Isso garante a originalidade e a aderência total ao conteúdo e metodologias do projeto, evitando o uso de materiais de terceiros.
Rolagem da Calculadora: Ajustes de CSS para rolagem.
Botão "Calcular": Destaque visual implementado.
Geração de Relatório (.md): Funcionalidade de download de resultados em formato Markdown foi implementada, transferindo corretamente todos os dados calculados e selecionados para o arquivo.
Backend (calculadora-api/main.py):

Inclusão de total_vertices: A API foi ajustada para incluir total_vertices na resposta JSON.
Base de Dados DOME_DATA: A estrutura da DOME_DATA no backend é detalhada com segments, num_segments, vertex_angles e total_vertices aninhados dentro de cada objeto de truncagem.
Acesso Seguro aos Dados: A lógica de acesso aos dados aninhados (dome_info.get(...)) foi aprimorada para evitar KeyError.
Mistério do Número de Vértices: Ênfase Absoluta e Crucial!
Problema Persistente: Apesar de todas as correções no código e múltiplos deployments, o campo "Número de Vértices" no frontend persiste em exibir "N/A". Os logs da API indicam que a chave total_vertices está frequentemente ausente da resposta JSON ou é retornada como um objeto vazio ({}). Isso ocorre mesmo para combinações onde o DOME_DATA no main.py local possui valores numéricos claros (ex: Icosaedro V3 3/8 deveria ter 46 vértices, V4 1/2 deveria ter 91).
Análise Técnica: A causa mais provável é uma inconsistência na versão do main.py e/ou da DOME_DATA que está realmente implantada e ativa na Cloud Function, ou um problema de caching profundo no ambiente de execução do Google Cloud. A linha total_vertices: total_vertices dentro do dicionário results no main.py é essencial para a inclusão desse dado na resposta da API. A ausência persistente desse valor nos logs de depuração da API é o maior entrave para a funcionalidade completa da calculadora. Este mistério exige uma depuração meticulosa no ambiente da Cloud Function, incluindo a verificação manual do código-fonte implantado e a análise dos logs de depuração da API para a saída exata (DEBUG: Resposta final da API: { ... }).
Múltiplas Implantações: Foi identificado que existem múltiplas instâncias da função calculadora-domo-api em diferentes regiões. Recomenda-se consolidar para uma única instância ativa para clareza e gestão de custos.
Erro ModuleNotFoundError / Container Healthcheck failed: Resolvidos ao garantir um requirements.txt minimalista e a ausência de importações desnecessárias do main.py que causavam falhas na inicialização do container.
Direção Futura e Próximos Ajustes Essenciais:

Para que a calculadora atinja seu potencial máximo e funcione como uma ferramenta robusta para pesquisa, os seguintes passos são cruciais:

Prioridade Máxima: Desvendar o Mistério do Número de Vértices (Backend).

Ação: Realizar uma verificação manual e exaustiva do main.py diretamente na aba "Código-Fonte" (Source) da função calculadora-domo-api no Google Cloud Console. Confirmar que a DOME_DATA no ambiente implantado está com os números de vértices corretos e que a linha total_vertices: total_vertices está presente e ativa no results retornado. Utilizar o print(f"DEBUG: Resposta final da API: {results}") nos logs para confirmar a saída exata da API e identificar a raiz da ausência do valor.
Filtragem de Menus no Frontend (calculadora.js).

Ação: Ajustar a lógica de populamento dos dropdowns para que somente as opções de Frequência e Truncagem para as quais o DOME_DATA (no backend) possui dados completos (segmentos, quantidades, ângulos e total_vertices) sejam exibidas. Isso evitará a seleção de combinações inválidas ou incompletas, melhorando a experiência do usuário e a robustez da calculadora.
Implementar o Desconto da Conexão no Comprimento Final da Vara (Frontend).

Ação: Modificar a lógica em displayResults para que o Comp. Final (m) de cada segmento seja calculado como Comprimento Calculado - (2 * Comprimento do Conector). O "Comprimento do Conector" deve ser (Diâmetro dos Vértices Estimado / 2). Este ajuste é vital para a precisão construtiva da estrutura final.
Consolidar Implantações da Cloud Function:

Ação: Remover as instâncias redundantes da calculadora-domo-api em regiões não utilizadas no Google Cloud Console, mantendo apenas a que está ativa e funcionando.
Avanços Futuros (Visão de Projeto):

A ideia original para a evolução desta calculadora vai além do dimensionamento geométrico e de materiais. Pretende-se que, a partir de estudos aprofundados das características físicas e mecânicas de diversas espécies de bambu, a ferramenta possa ser aprimorada para incorporar cálculos estruturais de engenharia.

Expansão para Análise Estrutural: A calculadora poderá indicar com precisão o peso suportável da cobertura, resistências a cargas de vento e neve, e outras aplicações que resultem em esforços e peso sobre a estrutura.
Integração de Propriedades do Bambu: Isso envolverá a inclusão de uma base de dados com informações sobre densidade, módulo de elasticidade, resistência à compressão, tração e flexão para diferentes espécies e diâmetros de bambu.
Análise de Estabilidade: A ferramenta poderá auxiliar na verificação da estabilidade da estrutura sob diferentes condições de carregamento.
Este avanço permitirá que a Calculadora de Domos Geodésicos se torne uma ferramenta de projeto ainda mais abrangente e cientificamente embasada, ampliando sua aplicabilidade em trabalhos de pesquisa e desenvolvimento de construções sustentáveis.

# Último código da main.py
# calculadora-api/main.py - VERSÃO FINAL E CORRIGIDA COM INFORMAÇÕES ADICIONAIS

import functions_framework
from flask import jsonify
import math

# SUA BASE DE DADOS COMPLETA, COM A SINTAXE CORRIGIDA
# Adicionado 'total_vertices' quando a informação estava disponível no documento fornecido.
# Para frequências e truncagens onde os dados detalhados não foram fornecidos (N/D),
# 'total_vertices' será retornado como 'N/D'.
DOME_DATA = {
    "Icosahedron": {
        "V1": {"truncation": {"2/3": {"segments": {"A": 1.05146}, "num_segments": {"A": 25}, "vertex_angles": {"A": 31.72}, "total_vertices": 11}}},
        "V2": {"truncation": {"1/2": {"segments": {"A": 0.54653, "B": 0.61803}, "num_segments": {"A": 30, "B": 35}, "vertex_angles": {"A": 15.86, "B": 18.00}, "total_vertices": 26}}},
        "V3": {"truncation": {
            "3/8": {"segments": {"A": 0.34862, "B": 0.40355, "C": 0.41241}, "num_segments": {"A": 30, "B": 40, "C": 50}, "vertex_angles": {"A": 10.04, "B": 11.64, "C": 11.90}, "total_vertices": 46},
            "5/8": {"segments": {"A": 0.34862, "B": 0.40355, "C": 0.41241}, "num_segments": {"A": 30, "B": 55, "C": 80}, "vertex_angles": {"A": 10.04, "B": 11.64, "C": 11.90}, "total_vertices": 61}
        }},
        "V4": {"truncation": {"1/2": {"segments": {"A": 0.25318, "B": 0.29453, "C": 0.29524, "D": 0.29859, "E": 0.31287, "F": 0.32492}, "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 70, "F": 30}, "vertex_angles": {"A": 7.27, "B": 8.47, "C": 8.49, "D": 8.59, "E": 9.00, "F": 9.35}, "total_vertices": 91}}},
        "L3": {"truncation": {"1/2": {"segments": {"A": 0.27590, "B": 0.28547, "C": 0.31287, "D": 0.32124, "E": 0.32492}, "num_segments": {"A": 60, "B": 60, "C": 70, "D": 30, "E": 30}, "vertex_angles": {"A": 7.93, "B": 8.21, "C": 9.00, "D": 9.24, "E": 9.35}, "total_vertices": 91}}},
        "V5": {"truncation": {
            "7/15": {"segments": {"A": 0.19815, "B": 0.22569, "C": 0.23160, "D": 0.23179, "E": 0.24509, "F": 0.24535, "G": 0.24724, "H": 0.25517, "I": 0.26160}, "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 50, "F": 10, "G": 60, "H": 50, "I": 30}, "vertex_angles": {"A": 5.69, "B": 6.48, "C": 6.65, "D": 6.66, "E": 7.04, "F": 7.05, "G": 7.10, "H": 7.33, "I": 7.52}, "total_vertices": 126},
            "8/15": {"segments": {"A": 0.19815, "B": 0.22569, "C": 0.23160, "D": 0.23179, "E": 0.24509, "F": 0.24535, "G": 0.24724, "H": 0.25517, "I": 0.26160}, "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 80, "F": 20, "G": 70, "H": 70, "I": 35}, "vertex_angles": {"A": 5.69, "B": 6.48, "C": 6.65, "D": 6.66, "E": 7.04, "F": 7.05, "G": 7.10, "H": 7.33, "I": 7.52}, "total_vertices": 151}
        }},
        "V6": {"truncation": {"1/2": {"segments": {"A": 0.16257, "B": 0.18191, "C": 0.18738, "D": 0.19048, "E": 0.19801, "F": 0.20282, "G": 0.20591, "H": 0.21535, "I": 0.21663}, "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 60, "F": 90, "G": 130, "H": 65, "I": 60}, "vertex_angles": {"A": 4.66, "B": 5.22, "C": 5.38, "D": 5.47, "E": 5.68, "F": 5.82, "G": 5.91, "H": 6.18, "I": 6.22}, "total_vertices": 196}}},
        "2V.3V": {"truncation": {"1/2": {"segments": {"A": 0.18212, "B": 0.18854, "C": 0.18922, "D": 0.18932, "E": 0.19125, "F": 0.20591, "G": 0.21321, "H": 0.21445, "I": 0.21535, "J": 0.21663}, "num_segments": {"A": 60, "B": 30, "C": 60, "D": 60, "E": 60, "F": 70, "G": 30, "H": 60, "I": 65, "J": 60}, "vertex_angles": {"A": 5.22, "B": 5.41, "C": 5.43, "D": 5.43, "E": 5.49, "F": 5.91, "G": 6.12, "H": 6.16, "I": 6.18, "J": 6.22}, "total_vertices": 196}}}
    },
    "Cube": {
        # Para V1-V4, os dados detalhados não estavam no documento, então o total_vertices também é N/D.
        "V1": {"truncation": {"N/D": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}},
        "V2": {"truncation": {"N/D": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}},
        "V3": {"truncation": {"N/D": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}},
        "V4": {"truncation": {"N/D": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}},
        "V5": {"truncation": {"~1/2": {"segments": {"A": 0.17629, "B": 0.19100, "C": 0.19686, "D": 0.19765, "E": 0.20103, "F": 0.20327, "G": 0.20588, "H": 0.21382, "I": 0.21400, "J": 0.21992, "K": 0.22028, "L": 0.22264, "M": 0.22437, "N": 0.24051, "O": 0.24834, "P": 0.25832, "Q": 0.26002, "R": 0.26089, "S": 0.27779, "T": 0.27793, "U": 0.28006}, "num_segments": {"A": 28, "B": 24, "C": 24, "D": 28, "E": 24, "F": 24, "G": 38, "H": 14, "I": 24, "J": 24, "K": 24, "L": 24, "M": 24, "N": 24, "O": 12, "P": 24, "Q": 14, "R": 24, "S": 24, "T": 12, "U": 7}, "vertex_angles": {"A": 5.06, "B": 5.48, "C": 5.65, "D": 5.67, "E": 5.77, "F": 5.83, "G": 5.91, "H": 6.14, "I": 6.14, "J": 6.31, "K": 6.32, "L": 6.39, "M": 6.44, "N": 6.91, "O": 7.13, "P": 7.42, "Q": 7.47, "R": 7.50, "S": 7.98, "T": 7.99, "U": 8.05}, "total_vertices": 166}}}} , # Adicionado total_vertices
    "Octahedron": {
        "V1": {"truncation": {"1/2": {"segments": {"A": 1.41421}, "num_segments": {"A": 8}, "vertex_angles": {"A": 45.00}, "total_vertices": 5}}},
        "V2": {"truncation": {"1/2": {"segments": {"A": 0.76537, "B": 1.00000}, "num_segments": {"A": 16, "B": 12}, "vertex_angles": {"A": 22.50, "B": 30.00}, "total_vertices": 13}}},
        "V3": {"truncation": {"1/2": {"segments": {"A": 0.45951, "B": 0.63246, "C": 0.67142}, "num_segments": {"A": 16, "B": 20, "C": 24}, "vertex_angles": {"A": 13.28, "B": 18.44, "C": 19.62}, "total_vertices": 25}}},
        # Para L3_3/8, L3_5/8, V4, V5, V6 Octahedron, os dados detalhados não estavam no documento.
        "L3_3/8": {"truncation": {"3/8": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}},
        "L3_5/8": {"truncation": {"5/8": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}},
        "V4": {"truncation": {"N/D": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}},
        "V5": {"truncation": {"N/D": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}},
        "V6": {"truncation": {"N/D": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}}
    },
    "Dodecahedron": {
        "L1": {"truncation": {"N/D": {"segments": {"A": 0.64085, "B": 0.71364}, "num_segments": {"A": 60, "B": 30}, "vertex_angles": {"N/D": "N/D"}, "total_vertices": 32}}}, # Adicionado total_vertices
        # Para L2, L2T Dodecahedron, os dados detalhados não estavam no documento.
        "L2": {"truncation": {"N/D": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}},
        "L2T": {"truncation": {"N/D": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}}
    },
    "Tetrahedron": {
        "L2T": {"truncation": {"N/D": {"segments": {"A": 0.91940, "B": 1.15470}, "num_segments": {"A": 14, "B": 7}, "vertex_angles": {"N/D": "N/D"}, "total_vertices": 10}}}, # Adicionado total_vertices
        # Para L3T Tetrahedron, os dados detalhados não estavam no documento.
        "L3T": {"truncation": {"N/D": {"segments": {}, "num_segments": {}, "vertex_angles": {}, "total_vertices": "N/D"}}}
    }
}


@functions_framework.http
def calculadora_domo_api(request):
    headers = {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Methods': 'POST, OPTIONS','Access-Control-Allow-Headers': 'Content-Type'}
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    if request.method != 'POST':
        return (jsonify({"error": "Método não permitido."}), 405, headers)

    request_json = request.get_json(silent=True)
    if not request_json:
        return (jsonify({"error": "Corpo da requisição inválido."}), 400, headers)

    try:
        diameter = float(request_json.get('diameter'))
        base_solid = request_json.get('base_solid')
        frequency = request_json.get('frequency')
        truncation = request_json.get('truncation')

        # Acesso mais seguro aos dados aninhados
        if base_solid not in DOME_DATA:
            raise KeyError(f"Sólido base '{base_solid}' não encontrado.")
        
        if frequency not in DOME_DATA[base_solid]:
            raise KeyError(f"Frequência '{frequency}' não encontrada para o sólido '{base_solid}'.")

        # Ajuste aqui para acessar a truncagem corretamente
        # dome_info é AGORA o dicionário da truncagem selecionada
        if truncation not in DOME_DATA[base_solid][frequency]['truncation']:
            raise KeyError(f"Truncagem '{truncation}' não encontrada para o sólido '{base_solid}' e frequência '{frequency}'.")
        
        # O dome_info agora é o dicionário de dados da truncagem, por exemplo:
        # {"segments": {...}, "num_segments": {...}, "vertex_angles": {...}, "total_vertices": 91}
        dome_info = DOME_DATA[base_solid][frequency]['truncation'][truncation]
        
        radius = diameter / 2.0
        
        # Garante que 'segments' seja um dicionário antes de iterar
        calculated_lengths = {
            key: (f"{radius * coeff:.4f}" if isinstance(coeff, (int, float)) else str(coeff))
            for key, coeff in dome_info.get('segments', {}).items()
        }

        # Garante que 'num_segments' seja um dicionário antes de somar os valores
        total_segments = sum(dome_info.get('num_segments', {}).values()) if dome_info.get('num_segments') else 0
        
        # **Ajuste aqui: Acessa total_vertices diretamente de dome_info, que AGORA é o nível correto**
        total_vertices = dome_info.get('total_vertices', 'N/D') 

        results = {
            "success": True,
            "segment_lengths": calculated_lengths,
            "num_segments": dome_info.get('num_segments', {}), # Retorna dicionário vazio se não houver
            "vertex_angles": dome_info.get('vertex_angles', {}), # Retorna dicionário vazio se não houver
            "total_segments": total_segments,
            "total_vertices": total_vertices # Inclui o número de vértices na resposta
        }
        print(f"DEBUG: Resposta final da API: {results}")
        response = jsonify(results)

    except (ValueError, TypeError) as e:
        response = jsonify({"success": False, "error": f"Erro nos dados de entrada ou cálculo: {str(e)}. Verifique o diâmetro, se é um número válido."})
    
    except KeyError as e:
        # Mensagem de erro mais específica devido às verificações em cascata
        response = jsonify({"success": False, "error": f"Combinação de Sólido/Frequência/Truncagem não encontrada. {e}. Certifique-se de que o Solid, Frequência e Truncagem selecionados estão corretos e que os dados para eles existem no DOME_DATA."})
    
    except Exception as e:
        response = jsonify({"success": False, "error": f"Ocorreu um erro inesperado no servidor: {str(e)}"})

    for header, value in headers.items():
        response.headers[header] = value
    return response

# Último código da calculadora.js

// docs/assets/js/calculadora.js - VERSÃO FINAL COMPLETA COM IMAGENS E MODAL (REVISADA)

document.addEventListener('DOMContentLoaded', () => {

    // A base de dados que o seu backend usa para popular os menus dinamicamente.
    const DOME_DATA = {
        "Icosahedron": {
            "V1": {"truncation": {"2/3": {}}},
            "V2": {"truncation": {"1/2": {}}},
            "V3": {"truncation": {
                "3/8": {},
                "5/8": {}
            }},
            "V4": {"truncation": {"1/2": {}}},
            "L3": {"truncation": {"1/2": {}}},
            "V5": {"truncation": {
                "7/15": {},
                "8/15": {}
            }},
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
        <div id="results-container-widget" style="display: none; margin-top: 1rem;">
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
    const calculatorCSS = `#calculator-fixed-box{position:fixed;bottom:20px;right:20px;background-color:#fff;border:1px solid #ccc;border-radius:8px;padding:15px;box-shadow:0 4px 8px rgba(0,0,0,0.15);width:300px;z-index:1000;font-size:14px; max-height: calc(100vh - 40px); overflow-y: auto;} #calculator-fixed-box h2{font-size:1.1rem; margin-top:0; text-align:center;} .form-group-widget{margin-bottom:10px;} .form-group-widget label{display:block;margin-bottom:5px;font-weight:bold;} .form-group-widget input, .form-group-widget select{width:100%;padding:8px;box-sizing:border-box;} #results-container-widget h4{margin-top:15px;margin-bottom:10px;border-top:1px solid #eee;padding-top:10px;} #results-container-widget table{width:100%;border-collapse:collapse;font-size:13px;} #results-container-widget th, #results-container-widget td{border:1px solid #ddd;padding:5px;text-align:left;}

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
    const apiUrl = 'https://us-central1-adroit-citadel-397215.cloudfunctions.net/calculadora-domo-api';

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

        // Não há mais desconto do conector como entrada. finalLengthM será calculado sem desconto.
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
                let totalLinearMetersCalculated = 0;
                let totalSegmentsCalculated = 0;
                // Calculamos finalLengthM sem o desconto do conector de entrada
                for (const key in data.segment_lengths) {
                    const calculatedLength = parseFloat(data.segment_lengths[key]);
                    const quantity = data.num_segments[key];
                    let finalLengthM = calculatedLength; // Não há mais desconto do conector de entrada
                    
                    totalLinearMetersCalculated += finalLengthM * quantity;
                    totalSegmentsCalculated += quantity;
                }
                lastTotalLinearMeters = totalLinearMetersCalculated;
                
                // Passa totalLinearMetersCalculated e totalSegmentsCalculated
                displayResults(data, diameter, poleDiameterCm, totalLinearMetersCalculated, totalSegmentsCalculated); 
                updateDiagramImage();
                downloadResultsButton.style.display = 'block';

                lastCalculatedData = data;
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

    // Removido 'connectorCutoffCm' dos parâmetros
    function displayResults(data, domeDiameter, poleDiameterCm, totalLinearMeters, totalSegments) {
        let tableHTML = '<table><thead><tr><th>Tipo</th><th>Comp. Final (m)</th><th>Qtd.</th><th>Ângulo (\u03B1)</th></tr></thead><tbody>';
        
        for (const key in data.segment_lengths) {
            const calculatedLength = parseFloat(data.segment_lengths[key]);
            const quantity = data.num_segments[key];
            const vertexAngle = data.vertex_angles[key];

            let finalLengthM = calculatedLength; // Não há mais desconto do conector de entrada

            tableHTML += `<tr><td>${key}</td><td>${typeof finalLengthM === 'number' ? finalLengthM.toFixed(4) : 'N/A'}</td><td>${quantity}</td><td>${vertexAngle !== 'N/D' ? vertexAngle.toFixed(2) + '\u00B0' : 'N/A'}</td></tr>`;
        }
        tableHTML += '</tbody></table>';
        resultsTableDiv.innerHTML = tableHTML;

        // ** Recursos Materiais **
        let materialHTML = '<h4>Recursos Materiais:</h4><ul>';

        // Garante que numVertices seja um número ou "N/A"
        const numVertices = typeof data.total_vertices === 'number' ? data.total_vertices : 'N/A'; 

        materialHTML += `<li>Número de Vértices: ${numVertices}</li>`;
        materialHTML += `<li>Número Total de Varas: ${totalSegments}</li>`;
        materialHTML += `<li>Total de Metros Lineares de Varas de Bambu: ${totalLinearMeters.toFixed(2)} m</li>`;
        
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
                puUg132aMl = 30 * totalLinearMeters;
            } else if (poleDiameterCm > 5 && poleDiameterCm <= 10) {
                puUg132aMl = 60 * totalLinearMeters;
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
                <li>A especificação do cabo de aço será determinada pela carga solicitada, espécie e diâmetro do bambu a ser utilizado. </li>
                <li>Os furos nas varas de bambu para a passagem do cabo devem ser feitos nas extremidades a um ângulo de 45° no sentido da entrada, com diâmetro correspondente à espessura do cabo. </li>
                <li>Serão realizados dois furos perpendiculares a 3cm da extremidade e dois furos perpendiculares a 5cm da extremidade. </li>
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
        const tableRows = resultsTableDiv.querySelectorAll('table tr');
        if (tableRows.length > 0) {
            let header = [];
            tableRows[0].querySelectorAll('th').forEach(th => header.push(th.textContent.trim()));
            markdownContent += `| ${header.join(' | ')} |\n`;
            markdownContent += `|${'---|'.repeat(header.length)}\n`;

            for (let i = 1; i < tableRows.length; i++) {
                let rowData = [];
                tableRows[i].querySelectorAll('td').forEach(td => rowData.push(td.textContent.trim()));
                markdownContent += `| ${rowData.join(' | ')} |\n`;
            }
            markdownContent += `\n`;
        }

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
        markdownContent += `- A especificação do cabo de aço será determinada pela carga solicitada, espécie e diâmetro do bambu a ser utilizado. \n`;
        markdownContent += `- Os furos nas varas de bambu para a passagem do cabo devem ser feitos nas extremidades a um ângulo de 45° no sentido da entrada, com diâmetro correspondente à espessura do cabo. \n`;
        markdownContent += `- Serão realizados dois furos perpendiculares a 3cm da extremidade e dois furos perpendiculares a 5cm da extremidade. \n`;
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
});

# DOME-DATA do Gcloud

Vá ao Google Cloud Console, na aba "CÓDIGO-FONTE" da sua função calculadora-domo-api (na região southamerica-east1, que parece ser a ativa).
Verifique se a linha total_vertices": total_vertices realmente existe no dicionário results do main.py exibido lá.
Verifique se a linha print(f"DEBUG: Resposta final da API: {results}") realmente existe antes do jsonify(results) no main.py exibido lá.
Se essas linhas NÃO EXISTIREM no código da Cloud Function (no console), isso significa que a versão mais recente do seu main.py não foi implantada corretamente.
Nesse caso, você precisa re-implantar o main.py do seu VS Code com a certeza de que ele tem todas as últimas alterações (incluindo o print de depuração).

gcloud functions deploy calculadora-api \
--runtime python39 \
--trigger-http \
--allow-unauthenticated \
--entry-point calculadora_api \
--source backend-api/ \
--region southamerica-east1

Memorial de Ajustes e Falhas da Calculadora de Domos Geodésicos (Versão FINAL)
Este memorial consolida o histórico de desenvolvimento, as melhorias implementadas, as falhas resolvidas e os próximos passos cruciais para a Calculadora de Domos Geodésicos do projeto Tecnologia Takwara. Ele também incorpora diretrizes para o desenvolvimento futuro, a produção de conteúdo original e prompts para assistentes de IA.

Status Atual (Junho de 2025):

A calculadora atingiu um estágio de funcionalidade robusta, com a comunicação API-frontend estabelecida, cálculos de materiais precisos, desconto de conexões e arredondamentos conforme as necessidades construtivas. O "mistério" do número de vértices foi desvendado.

Resumo das Melhorias Implementadas e Falhas Resolvidas:

Frontend (docs/assets/js/calculadora.js):

Injeção de HTML e CSS: A calculadora é injetada dinamicamente como um "widget" flutuante.
Menus Dinâmicos: A lógica para popular os dropdowns de "Sólido Base", "Frequência/Variante" e "Tipo de Esfera" foi implementada com base no DOME_DATA.
Cálculos de Materiais Avançados: Implementação de cálculos para número de vértices, total de metros lineares de varas, conectores, sapatilhas, cabo de aço, prensas cabo, arruelas, PU Vegetal (UG132A e Mamonex RD70), diâmetro estimado dos vértices e anéis de borracha.
Unidades de Medida: Conversão de ml para Litros para PU Vegetal acima de 1000ml implementada.
Diâmetro dos Vértices (Cálculo e Observação Crítica): O cálculo foi corrigido para 2 * (1.5 * Diâmetro da Vara (cm) + 0.4 cm), resultando em 15.80 cm para uma vara de 5cm, um "parâmetro real de construção" validado. A observação no rodapé e no Markdown foi atualizada para descrever este cálculo (6 varas dispostas circularmente, espaçamento de 4mm) e sua importância estrutural.
Desconto da Conexão e Arredondamento dos Comprimentos (Resolvido!):
Problema Anterior: A ausência de desconto da conexão no comprimento final da vara causava imprecisão construtiva, e os arredondamentos não eram padronizados.
Solução: Implementado o desconto do conector no cálculo do Comp. Final (m) (subtraindo 2 * (metade do diâmetro do vértice) de cada vara). A tabela de resultados agora inclui as colunas "Comp. Original (m)" e "Desconto Conector (m)" para clareza.
Arredondamento: A função customRound() foi ajustada para um arredondamento padrão para duas casas decimais (toFixed(2)), o que é mais robusto e aceitável para pequenas variações de até 5mm, dada a flexibilidade das conexões.
Entradas no Formulário: O campo "Desconto Conector" foi removido.
Exibição de Diagramas e Modal: Funcionalidade para exibir diagramas e um modal para visualização ampliada foram adicionadas.
Rolagem da Calculadora: Ajustes de CSS para rolagem e largura do box (width: 500px;).
Botão "Calcular": Destaque visual implementado.
Geração de Relatório (.md): Funcionalidade de download de resultados em formato Markdown, incluindo todas as novas colunas e valores processados.
Backend (calculadora-api/main.py):

Mistério do Número de Vértices (Resolvido!):
Problema Anterior: O campo "Número de Vértices" no frontend exibia "N/A" ou "undefined". Os logs da API indicavam que a chave total_vertices estava ausente da resposta JSON ou era retornada como um objeto vazio ({}).
Solução: Identificado que a causa raiz era uma inconsistência na versão do main.py implantada na Cloud Function (não contendo a linha total_vertices: total_vertices no dicionário results final) e/ou um problema de cache do ambiente. A correção do comando de deployment (--source backend-api/calculadora-api/) e a garantia de que a versão correta do main.py (com a linha total_vertices no results e o DEBUG print) foi implantada resolveram o problema. Os logs de depuração da API confirmaram que o valor agora é retornado corretamente.
Múltiplas Implantações: Identificado e recomendado a consolidação para uma única instância ativa.
Erro ModuleNotFoundError / Container Healthcheck failed: Resolvidos ao garantir um requirements.txt minimalista (functions-framework, Flask) e a ausência de importações desnecessárias do main.py (como langchain_community).
Direção Futura e Próximos Ajustes Essenciais:

Para que a calculadora atinja seu potencial máximo e funcione como uma ferramenta robusta para pesquisa, os seguintes passos são cruciais:

Refinar a DOME_DATA (Backend - Qualidade de Dados):

Ação: Revisar os coeficientes de segments no main.py para as frequências onde comprimentos finais muito próximos (ou idênticos) ainda são observados após o arredondamento. Se geometricamente possível e preciso, ajustar os coeficientes para que representem distinções reais e, se não, agrupar segmentos verdadeiramente idênticos. Isso garante a fidelidade geométrica da base de dados.
Filtragem Dinâmica de Menus no Frontend (calculadora.js).

Ação: Ajustar a lógica de populamento dos dropdowns de "Frequência/Variante" e "Tipo de Esfera" para que somente as opções para as quais o DOME_DATA (no backend) possui dados completos e válidos (i.e., chaves de segments, num_segments, vertex_angles e total_vertices com valores não "N/D" ou vazios) sejam exibidas. Isso evitará a seleção de combinações que resultam em "N/D" ou mensagens de "chave ausente", melhorando a experiência do usuário e a robustez da calculadora.
Consolidar Implantações da Cloud Function:

Ação: Remover as instâncias redundantes da calculadora-domo-api em regiões não utilizadas no Google Cloud Console, mantendo apenas a que está ativa e funcionando.
Avanços Futuros (Visão de Projeto):

A ideia original para a evolução desta calculadora vai além do dimensionamento geométrico e de materiais. Pretende-se que, a partir de estudos aprofundados das características físicas e mecânicas de espécies de bambu, a ferramenta possa incorporar cálculos estruturais de engenharia.

Expansão para Análise Estrutural: A calculadora poderá indicar com precisão o peso suportável da cobertura, resistências a cargas de vento e neve, e outras aplicações que resultem em esforços e peso sobre a estrutura. Isso envolverá a integração de dados sobre propriedades do bambu (densidade, módulo de elasticidade, resistência à compressão/tração/flexão) e a execução de algoritmos de análise estrutural.
Análise de Estabilidade: A ferramenta poderá auxiliar na verificação da estabilidade da estrutura sob diferentes condições de carregamento.
Este avanço permitirá que a Calculadora de Domos Geodésicos se torne uma ferramenta de projeto ainda mais abrangente e cientificamente embasada, ampliando sua aplicabilidade em trabalhos de pesquisa e desenvolvimento de construções sustentáveis.

Diretriz e Prompt para Geração de Imagens de Diagramas (Para Assistentes de IA/Designers):

Para garantir a originalidade e a alta qualidade do conteúdo visual do projeto Tecnologia Takwara, todas as imagens de diagramas de montagem e tipologias de domos devem ser geradas internamente pela equipe de design/assistentes de IA, e não extraídas de fontes externas.

Prompt Guia para Geração de Imagens:

**Objetivo:** Gerar um diagrama técnico-ilustrativo de um domo geodésico de bambu para a calculadora.

**Estilo Visual:**
* **Limpo e Claro:** Foco na clareza das formas e conexões.
* **Estilo "Desenho Técnico" com Toque Artístico:** Linhas bem definidas, mas com uma leve textura de bambu e conectores.
* **Paleta de Cores:** Cores naturais e neutras (tons de bambu, verde folha sutil, cinzas para conectores), com possíveis destaques para elementos específicos (ex: uma vara de um tipo 'A' destacada em uma cor suave para ilustração).
* **Perspectiva:** Geralmente uma perspectiva isométrica ou 3/4 que mostre a estrutura do domo e a complexidade das interconexões.

**Elementos a Incluir (para cada diagrama específico):**

1.  **Forma Geral do Domo:** Representação clara do sólido base (Icosaedro, Cubo, etc.), frequência (V1, V2, V3) e tipo de esfera/truncagem (1/2, 3/8, 2/3, N/D, etc.). A forma deve ser fiel à geometria correspondente.
2.  **Segmentos/Varas:** Mostrar as varas de bambu com sua cor e textura orgânica. Se houver diferentes tipos de segmentos (A, B, C...), eles podem ser sutilmente diferenciados (ex: varas de tipo 'A' com um tom ligeiramente diferente, ou uma leve etiqueta 'A' flutuante ao lado de algumas para exemplos).
3.  **Conexões/Vértices:**
    * Representar as uniões/conectores conforme o sistema descrito no Memorial (conexões semiflexíveis de aço cabeado, com sapatilhas e prensas).
    * Mostrar a forma como as varas se encontram no vértice, destacando o "diâmetro do vértice" (a união das 6 varas ao redor do eixo) e como o conector se integra.
    * Detalhes como arruelas de borracha e pré-tensionamento do cabo podem ser ilustrados em um "zoom in" se for um diagrama de detalhes.
4.  **Simplicidade e Clareza:** Evitar elementos distrativos. O foco deve ser na geometria e nas conexões.
5.  **Fundo:** Neutro (branco, cinza claro) para realçar o domo.

**Exemplos de Prompts Específicos (para o assistente de IA ou designer):**

* "Gerar diagrama de um Domo Geodésico Icosaedro V4 1/2. Foco na estrutura geral, mostrando os diferentes comprimentos de varas sutilmente. A conexão é a de aço cabeado, mas sem zoom."
* "Ilustrar um vértice de domo geodésico com 6 varas de bambu (diâmetro de 5cm) dispostas circularmente, com espaçamento de 4mm. O diagrama deve mostrar o conector no centro e o cabo de aço passando pelas varas. Perspectiva detalhada."
* "Diagrama de um Domo Octaedro V3 1/2, com representação clara das varas e as conexões em cada vértice."

**Formato de Saída:** Imagens PNG de alta resolução (ex: 600x400 pixels ou maior, mantendo a proporção).

---
