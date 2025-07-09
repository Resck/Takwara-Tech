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

# Nova Regex para extrair: Prefixo, Ícone Opcional, Nome de Exibição
# Captura 1: ([a-zA-Z0-9\.]+) -> O prefixo (ex: A1., A2.a.)
# Captura 2: (?:\[icon:([^\]]+)\]\s*)? -> O ícone opcional (grupo não-capturante para o colchete e nome do ícone)
# Captura 3: (.*) -> O restante do nome como nome de exibição
ICON_NAME_REGEX = re.compile(r'^([a-zA-Z0-9\.]+)\s*(?:\[icon:([^\]]+)\])?\s*(.*)$')

def extract_prefix_icon_and_name(name, entry_full_path):
    """
    Extrai prefixo, ícone (se presente) e nome de exibição de um nome de arquivo/pasta.
    Retorna (prefixo_original, ícone, nome_exibicao, nome_original, is_directory).
    """
    if name.startswith('#'):
        return None, None, None, None, False # Ignora itens comentados

    match = ICON_NAME_REGEX.match(name)
    if match:
        prefix = match.group(1)
        icon = match.group(2) # Pode ser None se não houver ícone
        display_name = match.group(3).strip() # Remove espaços em branco extras no final
        is_dir = os.path.isdir(entry_full_path)
        return prefix, icon, display_name, name, is_dir
    else:
        # Fallback se o padrão não for encontrado
        print(f"Aviso: Item '{name}' não seguiu o padrão de prefixo ou ícone esperado. Usando nome completo para exibição.")
        is_dir = os.path.isdir(entry_full_path)
        return name, None, name, name, is_dir # Sem prefixo, sem ícone, usa o nome completo.

def build_nav_structure(current_dir_full_path, current_dir_relative_path):
    temp_items = []
    entries = os.listdir(current_dir_full_path)

    for entry_name in entries:
        if entry_name.startswith('.'):
            continue

        entry_full_path = os.path.join(current_dir_full_path, entry_name)
        prefix, icon, display_name, original_name, is_dir = extract_prefix_icon_and_name(entry_name, entry_full_path)

        if prefix is None: # Item para ser ignorado
            continue

        entry_relative_path = os.path.join(current_dir_relative_path, original_name).replace('\\', '/')
        sort_key = parse_prefix_for_sort(prefix)

        if is_dir:
            sub_items_result = build_nav_structure(entry_full_path, entry_relative_path)
            if sub_items_result:
                nav_item_dict = {display_name: sub_items_result} # O nome da pasta é a chave do dicionário de subitens
                if icon:
                    # Para diretórios, o ícone vai diretamente no nó pai do menu
                    nav_item_dict[display_name] = {'icon': icon, 'children': sub_items_result}
                temp_items.append((sort_key, nav_item_dict))
        elif entry_name.endswith('.md'): # É um arquivo
            item_config = entry_relative_path # Por padrão, o valor é o link
            if icon:
                # Para itens folha (arquivos), o ícone é um campo adicional
                item_config = {'icon': icon, 'link': entry_relative_path}
            
            # Se o nome de exibição for diferente do nome original do arquivo (ex: com ícone)
            # O MkDocs precisa que o nome de exibição seja a chave do dicionário
            if display_name != original_name.replace('.md', '').replace('.txt', '').replace('.py', ''):
                 temp_items.append((sort_key, {display_name: item_config}))
            else:
                 temp_items.append((sort_key, {original_name.replace('.md', '').replace('.txt', '').replace('.py', ''): item_config}))

    sorted_temp_items = sorted(temp_items, key=lambda item: item[0])
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