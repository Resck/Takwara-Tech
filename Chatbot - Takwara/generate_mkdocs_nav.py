# /Users/fabiotakwara/Documents/GitHub/Takwara-Tech/Chatbot - Takwara/generate_mkdocs_nav.py
# -*- coding: utf-8 -*-
"""
Script para gerar automaticamente a seção 'nav:' do mkdocs.yml
com base na estrutura de pastas e nomes de arquivos na pasta 'docs/'.

A ordem e a hierarquia são definidas por prefixos alfanuméricos
(ex: A1., a1.1, A2.a) e a exclusão de itens em revisão é feita por '#' inicial.

Autor: Fabio Takwara
"""

import os
import yaml
import re

# --- Configurações ---
# O caminho para a pasta de documentação (onde estão seus arquivos .md e subpastas)
# Este script deve ser executado na raiz do repositório Takwara-Tech.
DOCS_DIR = 'docs'

# O caminho para o arquivo de configuração do MkDocs
MKDOCS_YML_PATH = 'mkdocs.yml'

# Regex para extrair o prefixo (letras, números, pontos) e o nome de exibição.
# Captura: ([a-zA-Z0-9\.]+) -> o prefixo
# Captura: \s+ -> um ou mais espaços após o prefixo
# Captura: (.*) -> o restante do nome como nome de exibição
PREFIX_REGEX = re.compile(r'^([a-zA-Z0-9\.]+)\s+(.*)$')

# --- Funções Auxiliares ---

def parse_prefix_for_sort(prefix):
    """
    Analisa um prefixo alfanumérico (ex: 'A2.a', 'a1.10') e retorna uma tupla
    para uso em ordenação. Trata partes numéricas como inteiros.
    Ex: 'A2.a' -> ('A', 2, 'a'), 'a1.10' -> ('a', 1, 10), 'B' -> ('B',)
    Isso garante que 'A10' venha depois de 'A2'.
    """
    parts = prefix.split('.')
    sort_key_parts = []
    for part in parts:
        if part.isdigit():
            sort_key_parts.append(int(part))
        else:
            sort_key_parts.append(part) # Mantém letras ou strings como estão
    return tuple(sort_key_parts)

def extract_prefix_and_name(name):
    """
    Extrai o prefixo de ordenação e o nome de exibição de um nome de arquivo/pasta.
    Retorna (prefixo_original, nome_exibicao, nome_original) ou (None, None, None) se ignorado.
    """
    if name.startswith('#'):
        # Ignora arquivos ou pastas comentados
        return None, None, None

    match = PREFIX_REGEX.match(name)
    if match:
        prefix = match.group(1)
        display_name = match.group(2)
        return prefix, display_name, name # Retorna o nome original para construir o caminho
    else:
        # Se o nome não corresponder ao padrão de prefixo, use o nome completo
        # para exibição e como prefixo de ordenação. (Caso de fallback, pode ser ajustado)
        print(f"Aviso: Item '{name}' na pasta docs/ não segue o padrão de prefixo (ex: 'A1. Nome'). Usando nome completo para exibição e ordenação.")
        return name, name, name # Use nome completo para exibir e ordenar

def build_nav_structure(current_dir_full_path, current_dir_relative_path):
    """
    Percorre recursivamente a estrutura de diretórios a partir do caminho completo
    e constrói a estrutura de lista/dicionário para a seção 'nav:' do MkDocs.
    Retorna uma lista de dicionários representando os itens de navegação neste nível.
    """
    temp_items = [] # Lista temporária para armazenar (chave_ordenacao, item_nav_dict)

    # Obtém a lista de entradas no diretório atual (arquivos e subpastas)
    # Não ordena aqui ainda, a ordenação será feita pela chave de ordenação extraída
    entries = os.listdir(current_dir_full_path)

    for entry_name in entries:
        # Ignora arquivos/pastas ocultos do sistema (ex: .DS_Store)
        if entry_name.startswith('.'):
            continue

        prefix, display_name, original_name = extract_prefix_and_name(entry_name)

        if prefix is None: # Item para ser ignorado (começa com '#')
            continue

        # Constrói os caminhos completo e relativo para a entrada atual
        entry_full_path = os.path.join(current_dir_full_path, original_name)
        entry_relative_path = os.path.join(current_dir_relative_path, original_name).replace('\\', '/') # Usa barras normais para caminhos do MkDocs

        # Obtém a chave de ordenação para o item atual
        sort_key = parse_prefix_for_sort(prefix)

        if os.path.isdir(entry_full_path):
            # É um diretório, faz a chamada recursiva para construir seus filhos
            sub_items = build_nav_structure(entry_full_path, entry_relative_path)
            if sub_items:
                # Se o subdiretório tiver itens válidos, adiciona como um item de menu pai
                temp_items.append((sort_key, {display_name: sub_items}))
            # Se o subdiretório estiver vazio ou só contiver itens ignorados, ele mesmo não é adicionado ao nav.
            # Ajuste: Se você quer que o diretório apareça mesmo vazio, remova o `if sub_items:`
            # e trate o caso de sub_items vazio na append.
        elif os.path.isfile(entry_full_path) and entry_name.endswith('.md'):
            # É um arquivo Markdown, adiciona como um item de menu folha (link)
            temp_items.append((sort_key, {display_name: entry_relative_path}))
        # Ignora outros tipos de arquivo

    # Ordena os itens deste nível com base nas chaves de ordenação
    sorted_temp_items = sorted(temp_items, key=lambda item: item[0])

    # Retorna apenas a lista de dicionários de itens de navegação
    nav_items = [item[1] for item in sorted_temp_items]

    return nav_items

# --- Execução Principal ---

if __name__ == "__main__":
    # Verifica se o diretório 'docs' existe
    if not os.path.isdir(DOCS_DIR):
        print(f"Erro: Diretório '{DOCS_DIR}' não encontrado na raiz do repositório.")
        exit(1)

    # Constrói a estrutura de navegação a partir da pasta 'docs'
    print(f"Construindo estrutura de navegação a partir de '{DOCS_DIR}'...")
    # A chamada inicial usa o caminho completo para DOCS_DIR e um caminho relativo vazio ''
    nav_structure = build_nav_structure(DOCS_DIR, '')

    # Carrega o conteúdo atual do mkdocs.yml
    try:
        with open(MKDOCS_YML_PATH, 'r', encoding='utf-8') as f:
            mkdocs_config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{MKDOCS_YML_PATH}' não encontrado na raiz do repositório.")
        print("Certifique-se de que está executando o script na pasta raiz do seu repositório.")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Erro ao analisar o arquivo '{MKDOCS_YML_PATH}': {e}")
        exit(1)

    # Substitui a seção 'nav:' no dicionário de configuração
    # Se 'nav' não existir, ele será criado.
    mkdocs_config['nav'] = nav_structure

    # Salva o conteúdo modificado de volta no mkdocs.yml
    try:
        with open(MKDOCS_YML_PATH, 'w', encoding='utf-8') as f:
            # Usa safe_dump para evitar injeção de código YAML
            # default_flow_style=False para formato de blocos (mais legível)
            # indent=2 para identação de 2 espaços
            # allow_unicode=True para garantir que caracteres especiais sejam salvos corretamente
            yaml.safe_dump(mkdocs_config, f, default_flow_style=False, indent=2, allow_unicode=True)
        print(f"Seção 'nav:' atualizada com sucesso em '{MKDOCS_YML_PATH}'.")
        print("Agora você pode executar 'mkdocs gh-deploy' para publicar o site atualizado.")
    except IOError as e:
        print(f"Erro ao escrever no arquivo '{MKDOCS_YML_PATH}': {e}")
        exit(1)