# Especificações Geométricas Detalhadas para Cúpulas Geodésicas: Coeficientes de Comprimento de Vareta, Quantidades e Ângulos de Vértice para Frequências V1-V6 e Truncagens Comuns, Baseadas em Icosaedro, Cubo e Outros Sólidos Platônicos

## Índice

*   [I. Introdução às Cúpulas Geodésicas](#i-introdução-às-cúpulas-geodésicas)
    *   [Terminologia e Conceitos Essenciais](#terminologia-e-conceitos-essenciais)
*   [II. Cúpulas Geodésicas Baseadas no Icosaedro](#ii-cúpulas-geodésicas-baseadas-no-icosaedro)
    *   [A. Cúpulas de Icosaedro V1](#a-cúpulas-de-icosaedro-v1)
    *   [B. Cúpulas de Icosaedro V2](#b-cúpulas-de-icosaedro-v2)
    *   [C. Cúpulas de Icosaedro V3](#c-cúpulas-de-icosaedro-v3)
    *   [D. Cúpulas de Icosaedro V4](#d-cúpulas-de-icosaedro-v4)
    *   [E. Cúpulas de Icosaedro V5](#e-cúpulas-de-icosaedro-v5)
    *   [F. Cúpulas de Icosaedro V6](#f-cúpulas-de-icosaedro-v6)
    *   [Tabela 1: Especificações de Cúpulas Geodésicas Baseadas no Icosaedro (Raio = 1.000)](#tabela-1-especificações-de-cúpulas-geodésicas-baseadas-no-icosaedro-raio--1000)
*   [III. Cúpulas Geodésicas Baseadas no Cubo](#iii-cúpulas-geodésicas-baseadas-no-cubo)
    *   [A. Cúpulas de Cubo V1-V4](#a-cúpulas-de-cubo-v1-v4)
    *   [B. Cúpulas de Cubo V5](#b-cúpulas-de-cubo-v5)
    *   [C. Cúpulas de Cubo V6](#c-cúpulas-de-cubo-v6)
    *   [Tabela 2: Especificações de Cúpulas Geodésicas Baseadas no Cubo (Raio = 1.000)](#tabela-2-especificações-de-cúpulas-geodésicas-baseadas-no-cubo-raio--1000)
*   [IV. Outras Cúpulas Geodésicas Baseadas em Sólidos Platônicos](#iv-outras-cúpulas-geodésicas-baseadas-em-sólidos-platônicos)
    *   [A. Cúpulas Geodésicas Baseadas no Octaedro](#a-cúpulas-geodésicas-baseadas-no-octaedro)
    *   [B. Cúpulas Geodésicas Baseadas no Dodecaedro](#b-cúpulas-geodésicas-baseadas-no-dodecaedro)
    *   [C. Cúpulas Geodésicas Baseadas no Tetraedro](#c-cúpulas-geodésicas-baseadas-no-tetraedro)
    *   [Tabela 3: Especificações de Cúpulas Geodésicas Baseadas em Outros Sólidos Platônicos (Raio = 1.000)](#tabela-3-especificações-de-cúpulas-geodésicas-baseadas-em-outros-sólidos-platônicos-raio--1000)
*   [V. Conclusões](#v-conclusões)
*   [Fontes usadas no relatório](#fontes-usadas-no-relatório)
*   [Fontes lidas, mas não usadas no relatório](#fontes-lidas-mas-não-usadas-no-relatório)

---

# Especificações Geométricas Detalhadas para Cúpulas Geodésicas: Coeficientes de Comprimento de Vareta, Quantidades e Ângulos de Vértice para Frequências V1-V6 e Truncagens Comuns, Baseadas em Icosaedro, Cubo e Outros Sólidos Platônicos

## I. Introdução às Cúpulas Geodésicas

As cúpulas geodésicas representam uma classe notável de estruturas esféricas, caracterizadas por uma rede de triângulos interconectados que lhes confere notável rigidez estrutural e eficiência material. O termo "geodésico" deriva da geodésia, a ciência da medição da Terra, e refere-se ao caminho mais curto entre dois pontos em uma superfície curva. Embora popularizadas por R. Buckminster Fuller no século XX, a primeira cúpula "geodésica" foi criada e patenteada por Walther Bauersfeld para Carl Zeiss em Jena, Alemanha, em 1922, mais de duas décadas antes dos desenvolvimentos de Fuller.

O princípio fundamental por trás da construção de uma cúpula geodésica envolve a triangulação de um poliedro base, cujos vértices são então projetados sobre a superfície de uma esfera. Este processo, conhecido como esferização ou projeção esférica, garante que todos os pontos da superfície da cúpula estejam a uma distância uniforme do seu centro, aproximando-se de uma esfera perfeita.

### Terminologia e Conceitos Essenciais

A compreensão das cúpulas geodésicas requer familiaridade com conceitos específicos que definem sua geometria e características estruturais:

- **Frequência (`nV` Notation):** A frequência, denotada como `nV` (onde 'n' é um número inteiro), indica o nível de subdivisão das faces triangulares do poliedro original. Por exemplo, uma cúpula 2V significa que cada aresta do triângulo original foi dividida em dois segmentos. À medida que a frequência aumenta, o número de triângulos na cúpula geodésica cresce, resultando em uma estrutura mais esférica e, geralmente, mais robusta. Contudo, frequências mais altas também implicam maior complexidade de construção e um número maior de varetas.

- **Notações Alternativas (`Ln` e V Concatenado):** Além da notação `nV` de Fuller, existem métodos alternativos de triangulação. A notação `Ln` (Nível 1, 2, etc.) e a notação `n0V.n1V...` (V concatenado) representam diferentes abordagens para subdividir o triângulo base. É fundamental reconhecer que, embora uma cúpula possa ser descrita por uma frequência geral (como 4V), a sua geometria interna e as características das varetas podem variar significativamente dependendo do método de triangulação empregado. Por exemplo, uma cúpula L3 não é idêntica a uma 4V, mas é similar, e uma 2V.2V também é similar a uma 4V, mas não igual. Essa distinção é crucial porque afeta diretamente o número de comprimentos de varetas únicos, seus valores específicos e a uniformidade geral da triangulação da cúpula, um parâmetro conhecido como "variância da vareta". Variantes como a L-notação e a V-concatenada frequentemente resultam em uma triangulação mais homogênea, com menor variância de vareta e, por vezes, menos tipos de varetas, o que pode simplificar a fabricação e melhorar a distribuição de carga. Para uma construção precisa, a especificação da frequência `nV` por si só pode ser insuficiente; o método de triangulação (por exemplo, Classe 1/Alternada, notação L ou V concatenada) deve ser detalhado para garantir as propriedades geométricas e estruturais desejadas.

- **Tipos de Truncagem:** A truncagem refere-se à porção da esfera completa que a cúpula representa. Os tipos comuns incluem:
    - **1/1 (Esfera Completa):** Uma estrutura esférica integral.
    - **1/2 (Hemisfério):** Metade de uma esfera, frequentemente referida como 4/8 ou 4/9.
    - **3/8 (Perfil Baixo):** Uma porção ligeiramente menor que um hemisfério, por vezes denominada 4/9.
    - **5/8 (Perfil Alto):** Uma porção ligeiramente maior que um hemisfério, por vezes denominada 5/9. É importante notar que cúpulas de frequência ímpar (como 3V e 5V) não possuem um "equador" natural e plano. Em vez disso, seu ponto de "hemisfério" natural se situa em 3/8 ou 5/8 da altura da esfera. Essa característica geométrica implica que, para obter uma base verdadeiramente plana em cúpulas de frequência ímpar, é necessário selecionar uma truncagem específica (3/8 ou 5/8) que se alinhe com um anel natural de vértices, em vez de simplesmente cortar no equador matemático. Isso afeta diretamente a relação altura-diâmetro da cúpula e sua usabilidade interna.

- **Coeficientes de Comprimento de Vareta e Escala:** Os comprimentos das varetas são apresentados como coeficientes normalizados, geralmente baseados em um raio de cúpula de 1.000 (ou diâmetro de 2.000). Uma propriedade fundamental desses coeficientes é sua escalabilidade linear. Se os comprimentos das varetas forem conhecidos para uma cúpula de um determinado diâmetro (por exemplo, 1 metro), eles podem ser multiplicados por uma constante (por exemplo, 20) para obter os comprimentos para uma cúpula maior (por exemplo, 20 metros). Isso significa que o usuário pode simplesmente multiplicar o coeficiente pelo raio desejado da cúpula (metade do diâmetro) para obter o comprimento real da vareta na unidade de medida escolhida.

- **Ângulos de Vértice (`α_vareta_`):** Estes ângulos referem-se às dobras necessárias nas extremidades de cada vareta para permitir a conexão adequada nos vértices e a formação da curvatura esférica. Em geometria esférica, ao contrário da geometria euclidiana plana, a soma dos ângulos internos de um triângulo é maior que 180 graus. Essa característica é fundamental para que os triângulos da cúpula se curvem para fora e os vértices sigam a superfície esférica.

- **Sólidos Platônicos como Estruturas Base:** Os cinco sólidos platônicos – Tetraedro, Cubo, Octaedro, Dodecaedro e Icosaedro – são poliedros regulares que podem servir como base para a construção de cúpulas geodésicas. O Icosaedro é o mais comum devido à sua inerente aproximação esférica e faces triangulares. No entanto, todos os sólidos platônicos podem ser triangulados para formar cúpulas geodésicas. Embora o Icosaedro seja amplamente utilizado, outras bases oferecem padrões geométricos e características estruturais únicas. Para poliedros com faces não triangulares (Cubo, Dodecaedro), uma etapa inicial de triangulação é necessária, o que influencia as configurações resultantes das varetas.

## II. Cúpulas Geodésicas Baseadas no Icosaedro

Esta seção detalha os coeficientes de comprimento de vareta, as quantidades e os ângulos de dobra para cúpulas baseadas no Icosaedro, considerando diversas frequências e tipos de truncagem. Todos os coeficientes são apresentados com base em um raio de cúpula de 1.000 (diâmetro de 2.000).

### A. Cúpulas de Icosaedro V1

A cúpula V1 Icosaedro é a forma mais simples, frequentemente referida como uma esfera 2/3. Ela se destaca por possuir apenas um tipo de vareta, o que simplifica enormemente a construção e resulta em uma variância de vareta de 0%, indicando perfeita uniformidade nos comprimentos das varetas.

- **Truncagem 1/1 (Esfera Completa) / 2/3:**
    - **Descrição:** Esta é a configuração mais básica, composta por um único tipo de vareta.
    - **Dados:**
        - Vareta A: Coeficiente de Comprimento = 1.05146, Quantidade = 25, Ângulo de Dobra = 31.72°
        - Total de Varetas: 25 (1 tipo)
        - Vértices/Conectores: 11 (5x 4-vias, 6x 5-vias)
        - Altura: 1.447 (72.36% do diâmetro)
        - Variância da Vareta: 0%

### B. Cúpulas de Icosaedro V2

A cúpula V2 Icosaedro é uma escolha comum e eficiente, capaz de formar um hemisfério verdadeiro (1/2 ou 50% da altura). Esta configuração utiliza dois tipos distintos de varetas, o que representa um aumento na complexidade em comparação com a V1, mas ainda mantém uma variância de vareta relativamente baixa.

- **Truncagem 1/1 (Esfera Completa) / 1/2 (Hemisfério):**
    - **Descrição:** Esta é uma cúpula hemisférica padrão, amplamente utilizada.
    - **Dados:**
        - Vareta A: Coeficiente de Comprimento = 0.54653, Quantidade = 30, Ângulo de Dobra = 15.86°
        - Vareta B: Coeficiente de Comprimento = 0.61803, Quantidade = 35, Ângulo de Dobra = 18.00°
        - Total de Varetas: 65 (2 tipos)
        - Vértices/Conectores: 26 (10x 4-vias, 6x 5-vias, 10x 6-vias)
        - Altura: 1.000 (50.00% do diâmetro)
        - Variância da Vareta: 13.1%

### C. Cúpulas de Icosaedro V3

As cúpulas V3 Icosaedro, sendo de frequência ímpar, não possuem um equador naturalmente plano, o que leva a truncagens de perfil mais baixo (3/8 ou 4/9) ou mais alto (5/8 ou 5/9). Ambas as configurações utilizam três tipos de varetas, mantendo uma variância de vareta consistente.

- **Truncagem 1/1 (Esfera Completa) / 3/8 (4/9):**
    - **Descrição:** Uma cúpula de perfil mais baixo, adequada para aplicações que exigem menor altura.
    - **Dados:**
        - Vareta A: Coeficiente de Comprimento = 0.34862, Quantidade = 30, Ângulo de Dobra = 10.04°
        - Vareta B: Coeficiente de Comprimento = 0.40355, Quantidade = 40, Ângulo de Dobra = 11.64°
        - Vareta C: Coeficiente de Comprimento = 0.41241, Quantidade = 50, Ângulo de Dobra = 11.90°
        - Total de Varetas: 120 (3 tipos)
        - Vértices/Conectores: 46 (15x 4-vias, 6x 5-vias, 25x 6-vias)
        - Altura: 0.828 (41.42% do diâmetro)
        - Variância da Vareta: 18.3%
- **Truncagem 1/1 (Esfera Completa) / 5/8 (5/9):**
    - **Descrição:** Uma cúpula de perfil mais alto, frequentemente utilizada para maximizar o espaço interno ou a altura.
    - **Dados:**
        - Vareta A: Coeficiente de Comprimento = 0.34862, Quantidade = 30, Ângulo de Dobra = 10.04°
        - Vareta B: Coeficiente de Comprimento = 0.40355, Quantidade = 55, Ângulo de Dobra = 11.64°
        - Vareta C: Coeficiente de Comprimento = 0.41241, Quantidade = 80, Ângulo de Dobra = 11.90°
        - Total de Varetas: 165 (3 tipos)
        - Vértices/Conectores: 61 (15x 4-vias, 6x 5-vias, 40x 6-vias)
        - Altura: 1.188 (59.38% do diâmetro)
        - Variância da Vareta: 18.3%

### D. Cúpulas de Icosaedro V4

As cúpulas V4 Icosaedro oferecem uma aproximação esférica superior e são tipicamente hemisféricas (1/2). Existem duas variantes principais: a V4 padrão e a L3. A comparação entre elas revela uma diferença importante na uniformidade da estrutura.

- **Truncagem 1/1 (Esfera Completa) / 1/2 (Hemisfério) - Variante V4:**
    - **Descrição:** Uma cúpula de frequência mais alta, com seis tipos de varetas.
    - **Dados:**
        - Vareta A: Coeficiente = 0.25318, Quantidade = 30, Ângulo = 7.27°
        - Vareta B: Coeficiente = 0.29453, Quantidade = 60, Ângulo = 8.47°
        - Vareta C: Coeficiente = 0.29524, Quantidade = 30, Ângulo = 8.49°
        - Vareta D: Coeficiente = 0.29859, Quantidade = 30, Ângulo = 8.59°
        - Vareta E: Coeficiente = 0.31287, Quantidade = 70, Ângulo = 9.00°
        - Vareta F: Coeficiente = 0.32492, Quantidade = 30, Ângulo = 9.35°
        - Total de Varetas: 250 (6 tipos)
        - Vértices/Conectores: 91 (20x 4-vias, 6x 5-vias, 65x 6-vias)
        - Altura: 1.000 (50.00% do diâmetro)
        - Variância da Vareta: 28.3%
- **Truncagem 1/1 (Esfera Completa) / 1/2 (Hemisfério) - Variante L3:**
    - **Descrição:** Uma variante otimizada da 4V, com menor variância de vareta e menos tipos de varetas.
    - **Dados:**
        - Vareta A: Coeficiente = 0.27590, Quantidade = 60, Ângulo = 7.93°
        - Vareta B: Coeficiente = 0.28547, Quantidade = 60, Ângulo = 8.21°
        - Vareta C: Coeficiente = 0.31287, Quantidade = 70, Ângulo = 9.00°
        - Vareta D: Coeficiente = 0.32124, Quantidade = 30, Ângulo = 9.24°
        - Vareta E: Coeficiente = 0.32492, Quantidade = 30, Ângulo = 9.35°
        - Total de Varetas: 250 (5 tipos)
        - Vértices/Conectores: 91 (20x 4-vias, 6x 5-vias, 65x 6-vias)
        - Altura: 1.000 (50.00% do diâmetro)
        - Variância da Vareta: 17.8%

A comparação entre as variantes V4 e L3 do Icosaedro, ambas resultando em cúpulas hemisféricas com 250 varetas, revela uma diferença notável na uniformidade estrutural. A variante L3 emprega 5 tipos de varetas e apresenta uma variância de vareta de 17.8%, enquanto a V4 utiliza 6 tipos de varetas e tem uma variância de 28.3%. Essa diferença na variância da vareta é significativa; uma menor variância indica que os comprimentos das varetas são mais próximos uns dos outros, resultando em triângulos mais uniformes e uma aproximação mais suave da forma esférica. Isso não apenas contribui para uma estética mais agradável, mas também pode implicar uma distribuição de carga mais homogênea e, consequentemente, melhor desempenho estrutural. A variante L3, com menos tipos de varetas e menor variância, oferece uma estrutura mais uniforme e simplifica a fabricação, tornando-a uma escolha mais vantajosa para a construção prática em comparação com a V4 direta.

### E. Cúpulas de Icosaedro V5

As cúpulas V5 Icosaedro, como as V3, são de frequência ímpar e, portanto, não possuem uma base naturalmente plana. Elas são apresentadas em truncagens de 7/15 (perfil mais baixo) e 8/15 (perfil mais alto), ambas com um número elevado de tipos de varetas e uma variância de vareta considerável.

- **Truncagem 1/1 (Esfera Completa) / 7/15:**
    - **Descrição:** Uma cúpula V5 de perfil mais baixo, com nove tipos de varetas.
    - **Dados:**
        - Vareta A: Coeficiente = 0.19815, Quantidade = 30, Ângulo = 5.69°
        - Vareta B: Coeficiente = 0.22569, Quantidade = 60, Ângulo = 6.48°
        - Vareta C: Coeficiente = 0.23160, Quantidade = 30, Ângulo = 6.65°
        - Vareta D: Coeficiente = 0.23179, Quantidade = 30, Ângulo = 6.66°
        - Vareta E: Coeficiente = 0.24509, Quantidade = 50, Ângulo = 7.04°
        - Vareta F: Coeficiente = 0.24535, Quantidade = 10, Ângulo = 7.05°
        - Vareta G: Coeficiente = 0.24724, Quantidade = 60, Ângulo = 7.10°
        - Vareta H: Coeficiente = 0.25517, Quantidade = 50, Ângulo = 7.33°
        - Vareta I: Coeficiente = 0.26160, Quantidade = 30, Ângulo = 7.52°
        - Total de Varetas: 350 (9 tipos)
        - Vértices/Conectores: 126 (25x 4-vias, 6x 5-vias, 95x 6-vias)
        - Altura: 0.896 (44.78% do diâmetro)
        - Variância da Vareta: 32.1%
- **Truncagem 1/1 (Esfera Completa) / 8/15:**
    - **Descrição:** Uma cúpula V5 de perfil mais alto, que compartilha os tipos de varetas com a 7/15, mas com quantidades diferentes.
    - **Dados:**
        - Vareta A: Coeficiente = 0.19815, Quantidade = 30, Ângulo = 5.69°
        - Vareta B: Coeficiente = 0.22569, Quantidade = 60, Ângulo = 6.48°
        - Vareta C: Coeficiente = 0.23160, Quantidade = 30, Ângulo = 6.65°
        - Vareta D: Coeficiente = 0.23179, Quantidade = 30, Ângulo = 6.66°
        - Vareta E: Coeficiente = 0.24509, Quantidade = 80, Ângulo = 7.04°
        - Vareta F: Coeficiente = 0.24535, Quantidade = 20, Ângulo = 7.05°
        - Vareta G: Coeficiente = 0.24724, Quantidade = 70, Ângulo = 7.10°
        - Vareta H: Coeficiente = 0.25517, Quantidade = 70, Ângulo = 7.33°
        - Vareta I: Coeficiente = 0.26160, Quantidade = 35, Ângulo = 7.52°
        - Total de Varetas: 425 (9 tipos)
        - Vértices/Conectores: 151 (25x 4-vias, 6x 5-vias, 120x 6-vias)
        - Altura: 1.111 (55.56% do diâmetro)
        - Variância da Vareta: 32.1%

### F. Cúpulas de Icosaedro V6

As cúpulas V6 Icosaedro representam uma alta frequência, proporcionando uma aproximação muito próxima de uma esfera. Estão disponíveis na variante V6 padrão e na variante concatenada 2V.3V, que oferece uma uniformidade superior.

- **Truncagem 1/1 (Esfera Completa) / 1/2 (Hemisfério) - Variante V6:**
    - **Descrição:** Uma cúpula de alta frequência com nove tipos de varetas.
    - **Dados:**
        - Vareta A: Coeficiente = 0.16257, Quantidade = 30, Ângulo = 4.66°
        - Vareta B: Coeficiente = 0.18191, Quantidade = 60, Ângulo = 5.22°
        - Vareta C: Coeficiente = 0.18738, Quantidade = 30, Ângulo = 5.38°
        - Vareta D: Coeficiente = 0.19048, Quantidade = 30, Ângulo = 5.47°
        - Vareta E: Coeficiente = 0.19801, Quantidade = 60, Ângulo = 5.68°
        - Vareta F: Coeficiente = 0.20282, Quantidade = 90, Ângulo = 5.82°
        - Vareta G: Coeficiente = 0.20591, Quantidade = 130, Ângulo = 5.91°
        - Vareta H: Coeficiente = 0.21535, Quantidade = 65, Ângulo = 6.18°
        - Vareta I: Coeficiente = 0.21663, Quantidade = 60, Ângulo = 6.22°
        - Total de Varetas: 555 (9 tipos)
        - Vértices/Conectores: 196 (30x 4-vias, 6x 5-vias, 160x 6-vias)
        - Altura: 1.000 (50.00% do diâmetro)
        - Variância da Vareta: 33.2%
- **Truncagem 1/1 (Esfera Completa) / 1/2 (Hemisfério) - Variante 2V.3V:**
    - **Descrição:** Uma variante concatenada da 6V, caracterizada por uma variância de vareta significativamente menor.
    - **Dados:**
        - Vareta A: Coeficiente = 0.18212, Quantidade = 60, Ângulo = 5.22°
        - Vareta B: Coeficiente = 0.18854, Quantidade = 30, Ângulo = 5.41°
        - Vareta C: Coeficiente = 0.18922, Quantidade = 60, Ângulo = 5.43°
        - Vareta D: Coeficiente = 0.18932, Quantidade = 60, Ângulo = 5.43°
        - Vareta E: Coeficiente = 0.19125, Quantidade = 60, Ângulo = 5.49°
        - Vareta F: Coeficiente = 0.20591, Quantidade = 70, Ângulo = 5.91°
        - Vareta G: Coeficiente = 0.21321, Quantidade = 30, Ângulo = 6.12°
        - Vareta H: Coeficiente = 0.21445, Quantidade = 60, Ângulo = 6.16°
        - Vareta I: Coeficiente = 0.21535, Quantidade = 65, Ângulo = 6.18°
        - Vareta J: Coeficiente = 0.21663, Quantidade = 60, Ângulo = 6.22°
        - Total de Varetas: 555 (10 tipos)
        - Vértices/Conectores: 196 (30x 4-vias, 6x 5-vias, 160x 6-vias)
        - Altura: 1.000 (50.00% do diâmetro)
        - Variância da Vareta: 18.9%

Ao comparar as cúpulas de Icosaedro 2V.3V e 6V, ambas com 555 varetas e formando hemisférios, observa-se uma diferença significativa na uniformidade estrutural. A variante 2V.3V possui 10 tipos de varetas e uma variância de vareta de 18.9%, enquanto a 6V tem 9 tipos de varetas e uma variância de 33.2%. Apesar de a 2V.3V ter um tipo de vareta a mais, sua variância de vareta consideravelmente menor indica que os comprimentos das varetas são muito mais uniformes. Isso se traduz em triângulos mais regulares e uma aproximação esférica superior. Essa observação demonstra que, para cúpulas de alta frequência, a otimização da variância da vareta pode ser um fator mais determinante para a qualidade da estrutura do que a simples minimização do número absoluto de tipos de varetas. A triangulação por "V concatenado" oferece uma aproximação de esfera superior em comparação com uma subdivisão V6 direta, resultando em uma cúpula mais robusta e esteticamente mais agradável.

### Tabela 1: Especificações de Cúpulas Geodésicas Baseadas no Icosaedro (Raio = 1.000)

| Frequência | Truncagem | Tipo de Vareta | Coeficiente de Comprimento | Quantidade | Ângulo de Dobra (`α_vareta_`) | Total de Varetas | Tipos de Varetas | Variância da Vareta | Altura (% Diâmetro) |
|---|---|---|---|---|---|---|---|---|---|
| V1 | 2/3 | A | 1.05146 | 25 | 31.72° | 25 | 1 | 0% | 72.36% |
| V2 | 1/2 | A | 0.54653 | 30 | 15.86° | 65 | 2 | 13.1% | 50.00% |
|  |  | B | 0.61803 | 35 | 18.00° |  |  |  |  |
| V3 | 3/8 (4/9) | A | 0.34862 | 30 | 10.04° | 120 | 3 | 18.3% | 41.42% |
|  |  | B | 0.40355 | 40 | 11.64° |  |  |  |  |
|  |  | C | 0.41241 | 50 | 11.90° |  |  |  |  |
| V3 | 5/8 (5/9) | A | 0.34862 | 30 | 10.04° | 165 | 3 | 18.3% | 59.38% |
|  |  | B | 0.40355 | 55 | 11.64° |  |  |  |  |
|  |  | C | 0.41241 | 80 | 11.90° |  |  |  |  |
| V4 | 1/2 | A | 0.25318 | 30 | 7.27° | 250 | 6 | 28.3% | 50.00% |
|  |  | B | 0.29453 | 60 | 8.47° |  |  |  |  |
|  |  | C | 0.29524 | 30 | 8.49° |  |  |  |  |
|  |  | D | 0.29859 | 30 | 8.59° |  |  |  |  |
|  |  | E | 0.31287 | 70 | 9.00° |  |  |  |  |
|  |  | F | 0.32492 | 30 | 9.35° |  |  |  |  |
| L3 | 1/2 | A | 0.27590 | 60 | 7.93° | 250 | 5 | 17.8% | 50.00% |
|  |  | B | 0.28547 | 60 | 8.21° |  |  |  |  |
|  |  | C | 0.31287 | 70 | 9.00° |  |  |  |  |
|  |  | D | 0.32124 | 30 | 9.24° |  |  |  |  |
|  |  | E | 0.32492 | 30 | 9.35° |  |  |  |  |
| V5 | 7/15 | A | 0.19815 | 30 | 5.69° | 350 | 9 | 32.1% | 44.78% |
|  |  | B | 0.22569 | 60 | 6.48° |  |  |  |  |
|  |  | C | 0.23160 | 30 | 6.65° |  |  |  |  |
|  |  | D | 0.23179 | 30 | 6.66° |  |  |  |  |
|  |  | E | 0.24509 | 50 | 7.04° |  |  |  |  |
|  |  | F | 0.24535 | 10 | 7.05° |  |  |  |  |
|  |  | G | 0.24724 | 60 | 7.10° |  |  |  |  |
|  |  | H | 0.25517 | 50 | 7.33° |  |  |  |  |
|  |  | I | 0.26160 | 30 | 7.52° |  |  |  |  |
| V5 | 8/15 | A | 0.19815 | 30 | 5.69° | 425 | 9 | 32.1% | 55.56% |
|  |  | B | 0.22569 | 60 | 6.48° |  |  |  |  |
|  |  | C | 0.23160 | 30 | 6.65° |  |  |  |  |
|  |  | D | 0.23179 | 30 | 6.66° |  |  |  |  |
|  |  | E | 0.24509 | 80 | 7.04° |  |  |  |  |
|  |  | F | 0.24535 | 20 | 7.05° |  |  |  |  |
|  |  | G | 0.24724 | 70 | 7.10° |  |  |  |  |
|  |  | H | 0.25517 | 70 | 7.33° |  |  |  |  |
|  |  | I | 0.26160 | 35 | 7.52° |  |  |  |  |
| V6 | 1/2 | A | 0.16257 | 30 | 4.66° | 555 | 9 | 33.2% | 50.00% |
|  |  | B | 0.18191 | 60 | 5.22° |  |  |  |  |
|  |  | C | 0.18738 | 30 | 5.38° |  |  |  |  |
|  |  | D | 0.19048 | 30 | 5.47° |  |  |  |  |
|  |  | E | 0.19801 | 60 | 5.68° |  |  |  |  |
|  |  | F | 0.20282 | 90 | 5.82° |  |  |  |  |
|  |  | G | 0.20591 | 130 | 5.91° |  |  |  |  |
|  |  | H | 0.21535 | 65 | 6.18° |  |  |  |  |
|  |  | I | 0.21663 | 60 | 6.22° |  |  |  |  |
| 2V.3V | 1/2 | A | 0.18212 | 60 | 5.22° | 555 | 10 | 18.9% | 50.00% |
|  |  | B | 0.18854 | 30 | 5.41° |  |  |  |  |
|  |  | C | 0.18922 | 60 | 5.43° |  |  |  |  |
|  |  | D | 0.18932 | 60 | 5.43° |  |  |  |  |
|  |  | E | 0.19125 | 60 | 5.49° |  |  |  |  |
|  |  | F | 0.20591 | 70 | 5.91° |  |  |  |  |
|  |  | G | 0.21321 | 30 | 6.12° |  |  |  |  |
|  |  | H | 0.21445 | 60 | 6.16° |  |  |  |  |
|  |  | I | 0.21535 | 65 | 6.18° |  |  |  |  |
|  |  | J | 0.21663 | 60 | 6.22° |  |  |  |  |

Exportar para as Planilhas

## III. Cúpulas Geodésicas Baseadas no Cubo

Esta seção apresenta os dados disponíveis para cúpulas geodésicas baseadas no Cubo, com coeficientes normalizados para um raio de 1.000 (diâmetro de 2.000). É importante notar que, para as frequências V1 a V4, os dados detalhados de comprimento e ângulo de dobra das varetas não foram diretamente extraídos das fontes fornecidas, que remetem principalmente a páginas externas para essas informações. No entanto, informações abrangentes para frequências mais altas (V5, V6 e variantes concatenadas) estavam disponíveis.

### A. Cúpulas de Cubo V1-V4

Para as cúpulas de Cubo de frequência V1 a V4, as informações detalhadas sobre os comprimentos e ângulos das varetas não foram diretamente acessíveis no material de pesquisa. Contudo, dados gerais sobre o número de varetas e a variância estrutural foram identificados, oferecendo uma visão preliminar da complexidade dessas estruturas.

- **V1 Cubo:**
    - **Informações Gerais:** Total de Varetas: 21, Tipos de Varetas: 2, Variância da Vareta: 25.6%.
    - *Comprimentos e ângulos detalhados não disponíveis no material fornecido.*
- **V2 Cubo:**
    - **Informações Gerais:** Total de Varetas: 78, Tipos de Varetas: 4, Variância da Vareta: 37.4%.
    - *Comprimentos e ângulos detalhados não disponíveis no material fornecido.*
- **V3 Cubo:**
    - **Informações Gerais:** Total de Varetas: 171, Tipos de Varetas: 10, Variância da Vareta: 50.1%.
    - *Comprimentos e ângulos detalhados não disponíveis no material fornecido.*
- **V4 Cubo:**
    - **Informações Gerais:** Total de Varetas: 300, Tipos de Varetas: 14, Variância da Vareta: 56.9%.
    - *Comprimentos e ângulos detalhados não disponíveis no material fornecido.*

### B. Cúpulas de Cubo V5

A cúpula V5 baseada no Cubo é uma estrutura de alta frequência que se aproxima de um hemisfério. Caracteriza-se por um número substancial de tipos de varetas e uma variância de vareta elevada, indicando uma complexidade considerável na fabricação e uma menor uniformidade geométrica em comparação com as cúpulas baseadas no Icosaedro.

- **Truncagem 1/1 (Esfera Completa) / ~1/2 (Hemisfério):**
    - **Descrição:** Cúpula de alta frequência baseada no Cubo, aproximando-se de um hemisfério.
    - **Dados:**
        - Vareta A: Coeficiente = 0.17629, Quantidade = 28, Ângulo = 5.06°
        - Vareta B: Coeficiente = 0.19100, Quantidade = 24, Ângulo = 5.48°
        - Vareta C: Coeficiente = 0.19686, Quantidade = 24, Ângulo = 5.65°
        - Vareta D: Coeficiente = 0.19765, Quantidade = 28, Ângulo = 5.67°
        - Vareta E: Coeficiente = 0.20103, Quantidade = 24, Ângulo = 5.77°
        - Vareta F: Coeficiente = 0.20327, Quantidade = 24, Ângulo = 5.83°
        - Vareta G: Coeficiente = 0.20588, Quantidade = 38, Ângulo = 5.91°
        - Vareta H: Coeficiente = 0.21382, Quantidade = 14, Ângulo = 6.14°
        - Vareta I: Coeficiente = 0.21400, Quantidade = 24, Ângulo = 6.14°
        - Vareta J: Coeficiente = 0.21992, Quantidade = 24, Ângulo = 6.31°
        - Vareta K: Coeficiente = 0.22028, Quantidade = 24, Ângulo = 6.32°
        - Vareta L: Coeficiente = 0.22264, Quantidade = 24, Ângulo = 6.39°
        - Vareta M: Coeficiente = 0.22437, Quantidade = 24, Ângulo = 6.44°
        - Vareta N: Coeficiente = 0.24051, Quantidade = 24, Ângulo = 6.91°
        - Vareta O: Coeficiente = 0.24834, Quantidade = 12, Ângulo = 7.13°
        - Vareta P: Coeficiente = 0.25832, Quantidade = 24, Ângulo = 7.42°
        - Vareta Q: Coeficiente = 0.26002, Quantidade = 14, Ângulo = 7.47°
        - Vareta R: Coeficiente = 0.26089, Quantidade = 24, Ângulo = 7.50°
        - Vareta S: Coeficiente = 0.27779, Quantidade = 24, Ângulo = 7.98°
        - Vareta T: Coeficiente = 0.27793, Quantidade = 12, Ângulo = 7.99°
        - Vareta U: Coeficiente = 0.28006, Quantidade = 7, Ângulo = 8.05°
        - Total de Varetas: 465 (21 tipos)
        - Vértices/Conectores: 166 (2x 3-vias, 30x 4-vias, 134x 6-vias)
        - Altura: 0.990 (49.51% do diâmetro)
        - Variância da Vareta: 58.9%

### C. Cúpulas de Cubo V6

As cúpulas V6 baseadas no Cubo representam uma das mais altas frequências para esta geometria, formando um hemisfério. Existem variantes padrão (V6) e concatenadas (2V.3V e 3V.2V), que demonstram como diferentes métodos de subdivisão podem influenciar a uniformidade estrutural.

- **Truncagem 1/1 (Esfera Completa) / 1/2 (Hemisfério) - Variante V6:**
    - **Descrição:** Uma cúpula de alta frequência com um grande número de tipos de varetas.
    - **Dados:**
        - Vareta A-AC (29 tipos): Coeficientes de Comprimento e Quantidades fornecidos na fonte.
        - Total de Varetas: 666 (29 tipos)
        - Vértices/Conectores: 235 (2x 3-vias, 36x 4-vias, 197x 6-vias)
        - Altura: 1.000 (50.00% do diâmetro)
        - Variância da Vareta: 63.1%
- **Truncagem 1/1 (Esfera Completa) / 1/2 (Hemisfério) - Variante 2V.3V:**
    - **Descrição:** Uma variante concatenada da 6V, com variância de vareta significativamente menor.
    - **Dados:**
        - Vareta A-AA (27 tipos): Coeficientes de Comprimento e Quantidades fornecidos na fonte.
        - Total de Varetas: 666 (27 tipos)
        - Vértices/Conectores: 235 (2x 3-vias, 36x 4-vias, 197x 6-vias)
        - Altura: 1.000 (50.00% do diâmetro)
        - Variância da Vareta: 44.4%
- **Truncagem 1/1 (Esfera Completa) / 1/2 (Hemisfério) - Variante 3V.2V:**
    - **Descrição:** Outra variante concatenada da 6V, com variância de vareta intermediária.
    - **Dados:**
        - Vareta A-V (22 tipos): Coeficientes de Comprimento e Quantidades fornecidos na fonte.
        - Total de Varetas: 666 (22 tipos)
        - Vértices/Conectores: 235 (2x 3-vias, 36x 4-vias, 197x 6-vias)
        - Altura: 1.000 (50.00% do diâmetro)
        - Variância da Vareta: 52.3%

As cúpulas baseadas no Cubo geralmente exibem uma variância de vareta consideravelmente maior em comparação com as cúpulas baseadas no Icosaedro, mesmo em frequências comparáveis. Por exemplo, a cúpula de Icosaedro 6V tem uma variância de 33.2%, enquanto a cúpula de Cubo 6V atinge 63.1%. Essa diferença na variância implica que as cúpulas de Cubo tendem a ter triângulos mais irregulares e, potencialmente, uma distribuição de tensão menos uniforme. Isso pode resultar em uma aparência mais facetada em vez de uma superfície esférica suave.

No entanto, as variantes concatenadas, como a 2V.3V para o Cubo, oferecem uma melhoria substancial na uniformidade, reduzindo a variância da vareta para 44.4% em comparação com os 63.1% da V6 padrão. Isso demonstra que, embora a base do Cubo possa introduzir desafios geométricos, a escolha de métodos de triangulação específicos pode mitigar parte dessa irregularidade. A grande quantidade de tipos de varetas (até 29 para a Cubo 6V) também representa um desafio significativo de fabricação, exigindo maior precisão e organização no corte e montagem. Para aplicações onde uma aparência esférica suave ou uma distribuição de carga otimizada são críticas, as cúpulas baseadas no Icosaedro são geralmente preferíveis. Se uma base de Cubo for selecionada, o uso de frequências mais altas e, em particular, variantes concatenadas, é essencial para reduzir a alta variância de vareta inerente a essa geometria.

### Tabela 2: Especificações de Cúpulas Geodésicas Baseadas no Cubo (Raio = 1.000)

| Frequência | Truncagem | Tipo de Vareta | Coeficiente de Comprimento | Quantidade | Ângulo de Dobra (`α_vareta_`) | Total de Varetas | Tipos de Varetas | Variância da Vareta | Altura (% Diâmetro) |
|---|---|---|---|---|---|---|---|---|---|
| V1 | N/D | N/D | N/D | N/D | N/D | 21 | 2 | 25.6% | N/D |
| V2 | N/D | N/D | N/D | N/D | N/D | 78 | 4 | 37.4% | N/D |
| V3 | N/D | N/D | N/D | N/D | N/D | 171 | 10 | 50.1% | N/D |
| V4 | N/D | N/D | N/D | N/D | N/D | 300 | 14 | 56.9% | N/D |
| V5 | ~1/2 | A | 0.17629 | 28 | 5.06° | 465 | 21 | 58.9% | 49.51% |
|  |  | B | 0.19100 | 24 | 5.48° |  |  |  |  |
|  |  | ... (19 mais) | ... | ... | ... |  |  |  |  |
| V6 | 1/2 | A | 0.14523 | 28 | 4.16° | 666 | 29 | 63.1% | 50.00% |
|  |  | B | 0.15547 | 24 | 4.46° |  |  |  |  |
|  |  | ... (27 mais) | ... | ... | ... |  |  |  |  |
| 2V.3V | 1/2 | A | 0.15768 | 56 | 4.52° | 666 | 27 | 44.4% | 50.00% |
|  |  | B | 0.16179 | 28 | 4.64° |  |  |  |  |
|  |  | ... (25 mais) | ... | ... | ... |  |  |  |  |
| 3V.2V | 1/2 | A | 0.15325 | 56 | 4.39° | 666 | 22 | 52.3% | 50.00% |
|  |  | B | 0.15508 | 24 | 4.45° |  |  |  |  |
|  |  | ... (20 mais) | ... | ... | ... |  |  |  |  |

Exportar para as Planilhas

*N/D: Dados detalhados não disponíveis no material de pesquisa fornecido.*

## IV. Outras Cúpulas Geodésicas Baseadas em Sólidos Platônicos

Além do Icosaedro e do Cubo, outros sólidos platônicos podem servir como base para cúpulas geodésicas, embora com características geométricas e práticas distintas. Esta seção apresenta os dados disponíveis para cúpulas baseadas no Octaedro, Dodecaedro e Tetraedro dentro das frequências V1-V6 e truncagens especificadas.

### A. Cúpulas Geodésicas Baseadas no Octaedro

O Octaedro é um poliedro com 8 faces triangulares, 6 vértices e 12 arestas. As cúpulas baseadas no Octaedro são tipicamente hemisféricas (1/2).

- **Truncagem 1/1 (Esfera Completa) / 1/2 (Hemisfério):**
    - **Variante V1:**
        - Vareta A: Coeficiente = 1.41421, Quantidade = 8, Ângulo = 45.00°
        - Total de Varetas: 8 (1 tipo)
        - Vértices/Conectores: 5 (4x 3-vias, 1x 4-vias)
        - Altura: 1.000 (50.00% do diâmetro)
        - Variância da Vareta: 0%
    - **Variante V2:**
        - Vareta A: Coeficiente = 0.76537, Quantidade = 16, Ângulo = 22.50°
        - Vareta B: Coeficiente = 1.00000, Quantidade = 12, Ângulo = 30.00°
        - Total de Varetas: 28 (2 tipos)
        - Vértices/Conectores: 13 (4x 3-vias, 5x 4-vias, 4x 6-vias)
        - Altura: 1.000 (50.00% do diâmetro)
        - Variância da Vareta: 30.7%
    - **Variante V3:**
        - Vareta A: Coeficiente = 0.45951, Quantidade = 16, Ângulo = 13.28°
        - Vareta B: Coeficiente = 0.63246, Quantidade = 20, Ângulo = 18.44°
        - Vareta C: Coeficiente = 0.67142, Quantidade = 24, Ângulo = 19.62°
        - Total de Varetas: 60 (3 tipos)
        - Vértices/Conectores: 25 (4x 3-vias, 9x 4-vias, 12x 6-vias)
        - Altura: 1.000 (50.00% do diâmetro)
        - Variância da Vareta: 46.1%
    - **Variante L3 3/8:**
        - Total de Varetas: 60, Tipos de Varetas: 5, Variância da Vareta: 48.0%.
        - *Comprimentos e ângulos detalhados não disponíveis no material fornecido.*
    - **Variante L3 5/8:**
        - Total de Varetas: 144, Tipos de Varetas: 5, Variância da Vareta: 48.0%.
        - *Comprimentos e ângulos detalhados não disponíveis no material fornecido.*
    - **Variantes V4, V5, V6:**
        - V4: 104 varetas, 6 tipos, 80.2% de variância.
        - V5: 160 varetas, 9 tipos, 92.9% de variância.
        - V6: 228 varetas, 9 tipos, 95.4% de variância.
        - *Comprimentos e ângulos detalhados não disponíveis no material fornecido.*

A variância da vareta para cúpulas baseadas no Octaedro aumenta significativamente com a frequência: 30.7% para V2, 46.1% para V3, 80.2% para V4, 92.9% para V5 e 95.4% para V6. Esses valores são consideravelmente mais altos do que os observados em cúpulas de Icosaedro de frequências comparáveis. Essa alta variância da vareta indica uma aproximação menos uniforme de uma esfera em comparação com os *designs* baseados no Icosaedro. Isso pode resultar em uma distribuição de tensão menos homogênea e uma aparência mais facetada. Embora as cúpulas de Octaedro possam oferecer simplicidade em frequências mais baixas (menos varetas), sua uniformidade geométrica se deteriora rapidamente com o aumento da frequência. Para aplicações que exigem alta esfericidade e distribuição de carga uniforme, as cúpulas baseadas no Icosaedro são geralmente preferíveis. As cúpulas de Octaedro podem ser adequadas para estruturas menores e mais simples, onde a alta esfericidade não é o requisito principal.

### B. Cúpulas Geodésicas Baseadas no Dodecaedro

O Dodecaedro possui 12 faces pentagonais, 20 vértices e 30 arestas. O material de pesquisa não forneceu dados específicos para as cúpulas baseadas no Dodecaedro usando a notação V (V1-V6) ou tipos de truncagem explícitos. No entanto, dados para variantes L-notation foram encontrados.

- **Variante L1 (Dodecaedro Geodésico L1):**
    - **Descrição:** Uma cúpula básica baseada no Dodecaedro.
    - Vareta A: Coeficiente = 0.64085, Quantidade = 60
    - Vareta B: Coeficiente = 0.71364, Quantidade = 30
    - Total de Varetas: 90 (2 tipos)
    - Vértices/Conectores: 32 (12x 5-vias, 20x 6-vias)
    - Variância da Vareta: 11.4%
- **Variante L2 (Dodecaedro Geodésico L2):**
    - **Descrição:** Uma subdivisão mais alta do Dodecaedro.
    - Vareta A: Coeficiente = 0.32474, Quantidade = 120
    - Vareta B: Coeficiente = 0.34034, Quantidade = 120
    - Vareta C: Coeficiente = 0.36284, Quantidade = 60
    - Vareta D: Coeficiente = 0.37668, Quantidade = 60
    - Total de Varetas: 360 (4 tipos)
    - Vértices/Conectores: 122 (12x 5-vias, 110x 6-vias)
    - Variância da Vareta: 16.0%
- **Variante L2T (Dodecaedro Geodésico L2T):**
    - **Descrição:** Uma variante "triaconizada" do Dodecaedro.
    - Vareta A-F (6 tipos): Coeficientes de Comprimento e Quantidades fornecidos na fonte.
    - Total de Varetas: 540 (6 tipos)
    - Vértices/Conectores: 182 (90x 4-vias, 60x 6-vias, 12x 10-vias, 20x 12-vias)
    - Variância da Vareta: 113.1%

A variante L2T do Dodecaedro apresenta uma variância de vareta extremamente alta, de 113.1%. Além disso, essa variante introduz conectores de 10 e 12 vias, que são significativamente mais complexos do que os conectores comuns de 4, 5 ou 6 vias observados em outras cúpulas. Embora as variantes L1 e L2 do Dodecaedro demonstrem uma variância relativamente baixa (11.4% e 16.0%, respectivamente), a L2T introduz uma irregularidade e complexidade consideráveis em suas conexões. Isso sugere que certas metodologias de triangulação, embora matematicamente viáveis, podem não ser práticas ou desejáveis para a construção física devido à extrema variação nos comprimentos das varetas e à necessidade de conectores especializados. Uma alta variância de vareta e tipos de conectores complexos podem aumentar substancialmente a dificuldade e o custo de fabricação, e potencialmente resultar em estruturas menos estáveis.

### C. Cúpulas Geodésicas Baseadas no Tetraedro

O Tetraedro é o poliedro mais simples, com 4 faces triangulares, 4 vértices e 6 arestas. A "geodesização" direta do Tetraedro resulta em uma esfera distorcida, e apenas as variantes "triaconizadas" (L-notation) são consideradas adequadas no material de pesquisa. Os ângulos de dobra não foram fornecidos para estas variantes. Não há dados de notação V (V1-V6) para cúpulas baseadas no Tetraedro.

- **Variante L2T (Cúpula de Tetraedro Geodésico L2T):**
    - **Descrição:** Uma cúpula de Tetraedro "triaconizada".
    - Vareta A: Coeficiente = 0.91940, Quantidade = 14
    - Vareta B: Coeficiente = 1.15470, Quantidade = 7
    - Total de Varetas: 21 (2 tipos)
    - Vértices/Conectores: 10 (2x 3-vias, 6x 4-vias, 2x 6-vias)
    - Variância da Vareta: 25.7%
    - *Ângulos de dobra não explicitamente fornecidos.*
- **Variante L3T (Cúpula de Tetraedro Geodésico L3T):**
    - **Descrição:** Uma subdivisão mais alta da cúpula de Tetraedro "triaconizada".
    - Vareta A: Coeficiente = 0.29239, Quantidade = 12
    - Vareta B: Coeficiente = 0.35693, Quantidade = 24
    - Vareta C: Coeficiente = 0.47313, Quantidade = 28
    - Vareta D: Coeficiente = 0.48701, Quantidade = 12
    - Vareta E: Coeficiente = 0.60581, Quantidade = 14
    - Vareta F: Coeficiente = 0.66092, Quantidade = 24
    - Total de Varetas: 114 (6 tipos)
    - Vértices/Conectores: 43 (6x 3-vias, 15x 4-vias, 2x 5-vias, 12x 6-vias, 4x 7-vias, 2x 8-vias, 2x 12-vias)
    - Variância da Vareta: 126.4%
    - *Ângulos de dobra não explicitamente fornecidos.*

A variância da vareta para a cúpula de Tetraedro L3T é extremamente alta, atingindo 126.4%. Essa é a maior variância observada entre todos os tipos de cúpulas analisados. Uma variância tão extrema implica faces triangulares altamente irregulares e uma distribuição muito desigual de material e tensão. Isso tornaria a construção extremamente difícil, devido à grande quantidade de peças altamente dissimilares, e provavelmente resultaria em uma cúpula que está longe de ser esférica e que pode ter sua integridade estrutural comprometida. A utilidade de tal cúpula para fins gerais é questionável, apesar de ser matematicamente derivável. Isso ressalta que, embora matematicamente possíveis, algumas derivações de cúpulas geodésicas a partir de sólidos platônicos, particularmente o Tetraedro, levam a *designs* altamente impraticáveis devido à variância extrema das varetas.

### Tabela 3: Especificações de Cúpulas Geodésicas Baseadas em Outros Sólidos Platônicos (Raio = 1.000)

| Poliedro Base | Frequência | Truncagem | Tipo de Vareta | Coeficiente de Comprimento | Quantidade | Ângulo de Dobra (`α_vareta_`) | Total de Varetas | Tipos de Varetas | Variância da Vareta | Altura (% Diâmetro) |
|---|---|---|---|---|---|---|---|---|---|---|
| Octaedro | V1 | 1/2 | A | 1.41421 | 8 | 45.00° | 8 | 1 | 0% | 50.00% |
| Octaedro | V2 | 1/2 | A | 0.76537 | 16 | 22.50° | 28 | 2 | 30.7% | 50.00% |
|  |  |  | B | 1.00000 | 12 | 30.00° |  |  |  |  |
| Octaedro | V3 | 1/2 | A | 0.45951 | 16 | 13.28° | 60 | 3 | 46.1% | 50.00% |
|  |  |  | B | 0.63246 | 20 | 18.44° |  |  |  |  |
|  |  |  | C | 0.67142 | 24 | 19.62° |  |  |  |  |
| Dodecaedro | L1 | N/D | A | 0.64085 | 60 | N/D | 90 | 2 | 11.4% | N/D |
|  |  |  | B | 0.71364 | 30 | N/D |  |  |  |  |
| Dodecaedro | L2 | N/D | A | 0.32474 | 120 | N/D | 360 | 4 | 16.0% | N/D |
|  |  |  | B | 0.34034 | 120 | N/D |  |  |  |  |
|  |  |  | C | 0.36284 | 60 | N/D |  |  |  |  |
|  |  |  | D | 0.37668 | 60 | N/D |  |  |  |  |
| Dodecaedro | L2T | N/D | A | 0.19071 | 60 | N/D | 540 | 6 | 113.1% | N/D |
|  |  |  | B | 0.21151 | 120 | N/D |  |  |  |  |
|  |  |  | ... (4 mais) | ... | ... | ... |  |  |  |  |
| Tetraedro | L2T | N/D | A | 0.91940 | 14 | N/D | 21 | 2 | 25.7% | N/D |
|  |  |  | B | 1.15470 | 7 | N/D |  |  |  |  |
| Tetraedro | L3T | N/D | A | 0.29239 | 12 | N/D | 114 | 6 | 126.4% | N/D |
|  |  |  | B | 0.35693 | 24 | N/D |  |  |  |  |
|  |  |  | ... (4 mais) | ... | ... | ... |  |  |  |  |

Exportar para as Planilhas

*N/D: Dados detalhados ou truncagem não disponíveis no material de pesquisa fornecido.*

## V. Conclusões

A análise detalhada dos coeficientes de comprimento de vareta, quantidades e ângulos de vértice para cúpulas geodésicas de diversas frequências e truncagens, baseadas em diferentes sólidos platônicos, revela uma complexa interação entre a geometria teórica e a praticidade construtiva.

Em primeiro lugar, a escolha do poliedro base tem um impacto profundo nas características da cúpula. O **Icosaedro** emerge como a base mais versátil e geralmente mais eficiente para a construção de cúpulas geodésicas. Suas derivações, especialmente as variantes de frequência mais alta (V4, V5, V6) e as otimizações como L3 e 2V.3V, oferecem uma excelente aproximação esférica com variâncias de vareta relativamente baixas. A baixa variância de vareta é um indicador crítico de uniformidade estrutural e estética, resultando em triângulos mais regulares e uma distribuição de carga mais homogênea. Para projetos que priorizam a esfericidade, a eficiência material e a facilidade de montagem (devido a um número gerenciável de tipos de varetas), as cúpulas baseadas no Icosaedro são a escolha mais robusta.

Em contraste, as cúpulas baseadas no **Cubo** e no **Octaedro** tendem a apresentar variâncias de vareta significativamente mais altas, especialmente em frequências elevadas. Embora matematicamente válidas, essas geometrias resultam em uma aproximação esférica menos uniforme e um número maior de tipos de varetas, o que pode aumentar a complexidade de fabricação e potencialmente afetar a distribuição de tensões na estrutura. Para cúpulas baseadas no Cubo, as variantes concatenadas (como 2V.3V) demonstram uma melhoria notável na uniformidade, reduzindo a variância da vareta e tornando-as mais viáveis para construção do que suas contrapartes V-notation diretas.

A exploração de outras bases, como o **Dodecaedro** e o **Tetraedro**, revela desafios adicionais. Embora as variantes L1 e L2 do Dodecaedro mostrem boa uniformidade, a variante L2T apresenta uma variância de vareta extremamente alta e a necessidade de conectores complexos, o que a torna impraticável. As cúpulas baseadas no **Tetraedro**, em particular a L3T, exibem a maior variância de vareta entre todas as geometrias analisadas. Essa irregularidade extrema implica um *design* que é, na prática, inviável para a maioria das aplicações, devido à dificuldade de fabricação e à provável deficiência estrutural.

A distinção entre as notações de frequência (`nV` vs. `Ln` vs. V concatenado) é um fator crucial. Diferentes métodos de subdivisão, mesmo que resultem em frequências nominais similares, produzem geometrias internas distintas que afetam diretamente a variância da vareta e o número de tipos de varetas. A escolha de uma variante com menor variância simplifica o processo de corte e montagem e pode otimizar o desempenho estrutural.

Por fim, a truncagem da cúpula é um aspecto prático que determina a porção da esfera utilizada. Para cúpulas de frequência ímpar, a ausência de um equador naturalmente plano exige a seleção cuidadosa de truncagens como 3/8 ou 5/8 para garantir uma base estável e nivelada.

Em suma, a seleção da geometria de uma cúpula geodésica deve ser uma decisão informada, considerando não apenas a frequência e o poliedro base, mas também a variância da vareta, o número de tipos de varetas e a complexidade dos conectores. Embora todos os sólidos platônicos possam gerar cúpulas, o Icosaedro oferece as soluções mais equilibradas e práticas para a maioria dos projetos, com as variantes otimizadas proporcionando a melhor combinação de esfericidade, uniformidade e viabilidade construtiva.

## Fontes usadas no relatório

- [ebsco.com - Polyhedron/Polyhedra | EBSCO Research Starters](https://www.ebsco.com/research-starters/mathematics/polyhedronpolyhedra)
- [pacificdomes.com - Geodesic Dome Frequencies Explained](https://pacificdomes.com/knowledge-base/geodesic-dome-frequencies-explained/)
- [domerama.com - 3V Geodesic Dome Calculators - Domerama](http://www.domerama.com/calculators/3v-geodesic-dome-calculator/)
- [mathworld.wolfram.com - Geodesic Dome -- from Wolfram MathWorld](https://mathworld.wolfram.com/GeodesicDome.html)
- [sonostarhub.com - How To Choose The Right Geodesic Dome Kit - Sonostarhub](https://www.sonostarhub.com/pages/how-to-choose-the-right-sonostar-kit)
- [simplydifferently.org - Geodesic Polyhedra - SimplyDifferently.org](https://www.simplydifferently.org/Geodesic_Polyhedra)
- [mathcircle.berkeley.edu - Geodesic Domes - Berkeley Math Circle](https://mathcircle.berkeley.edu/sites/default/files/BMC6/ps0405/geodesic.pdf)
- [simplydifferently.org - The Octahedron - SimplyDifferently.org: Geodesic Dome Notes & Calculator](https://www.simplydifferently.org/Geodesic_Dome_Notes?page=6) *
- [simplydifferently.org - SimplyDifferently.org: Geodesic Polyhedra](https://simplydifferently.org/Geodesic_Polyhedra?page=11) *
- [simplydifferently.org - 5V 7/15 Icosahedron Dome - SimplyDifferently.org: Geodesic Dome Notes & Calculator](https://www.simplydifferently.org/Geodesic_Dome_Notes?page=4) *
- [domerama.com - Leveling the base of a dome - Domerama](http://www.domerama.com/dome-basics/odd-frequency-geodesic-domes-and-flat-base-at-the-hemisphere/)
- [simplydifferently.org - SimplyDifferently.org: Geodesic Dome Notes & Calculator](https://simplydifferently.org/Geodesic_Dome_Notes?page=4) *
- [simplydifferently.org - SimplyDifferently.org: Geodesic Dome Notes & Calculator](https://simplydifferently.org/Geodesic_Dome_Notes?page=6) *
- [simplydifferently.org - SimplyDifferently.org: Geodesic Dome Notes & Calculator](https://simplydifferently.org/Geodesic_Dome_Notes?page=8) *
- [simplydifferently.org - SimplyDifferently.org: Geodesic Dome Notes & Calculator](https://simplydifferently.org/Geodesic_Dome_Notes?page=1) *
- [simplydifferently.org - SimplyDifferently.org: Geodesic Dome Notes & Calculator](https://simplydifferently.org/Geodesic_Dome_Notes?page=7) *
- [simplydifferently.org - SimplyDifferently.org: Geodesic Dome Notes & Calculator](https://simplydifferently.org/Geodesic_Dome_Notes?page=5) *
- [simplydifferently.org - SimplyDifferently.org: Geodesic Dome Notes & Calculator](https://simplydifferently.org/Geodesic_Dome_Notes?page=10) *
- [simplydifferently.org - SimplyDifferently.org: Geodesic Dome Notes & Calculator](https://simplydifferently.org/Geodesic_Dome_Notes?page=9) *
- [simplydifferently.org - Polyhedra Notes - SimplyDifferently.org](https://simplydifferently.org/Polyhedra_Notes)
- [simplydifferently.org - Geodesic Polyhedra - SimplyDifferently.org](https://simplydifferently.org/Geodesic_Polyhedra)
- [simplydifferently.org - SimplyDifferently.org: Geodesic Dome Notes & Calculator](https://simplydifferently.org/Geodesic_Dome_Notes?page=12) *
- [domerama.com - 1v Geodesic Dome Calculator - Domerama](http://www.domerama.com/calculators/1v-geodesic-dome-calculator/)
- [domerama.com - 2V Geodesic Dome Calculator - Domerama](http://www.domerama.com/calculators/2v-geodesic-dome-calculator/)
- [simplydifferently.org - Geodesic Dome Notes & Calculator - SimplyDifferently.org](https://simplydifferently.org/Geodesic_Dome_Notes?page=2) *
- [dahp.wa.gov - Domebook 2 - 1971](https://dahp.wa.gov/sites/default/files/Domebook_2_1971smaller.pdf)
- [simplydifferently.org - Geodesic Dome Notes & Calculator - SimplyDifferently.org](https://simplydifferently.org/Geodesic_Dome_Notes?page=3) *
- [en.wikipedia.org - Geodesic dome - Wikipedia](https://en.wikipedia.org/wiki/Geodesic_dome)
- [ziptiedomes.com - What is Geodesic Dome Frequency, An Explanation - Frequently Asked Questions for Zip Tie Domes](https://www.ziptiedomes.com/faq/What-Is-Geodesic-Dome-Frequency-Explained.htm)
- [drishti-svnit.github.io - Geodesic Dome - GitHub Pages](https://drishti-svnit.github.io/CIVIL/documentation/geodesic%20dome%20\(1\)-converted.pdf)
