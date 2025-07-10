# -*- coding: utf-8 -*-
"""
Script para gerar automaticamente a seção 'nav:' do mkdocs.yml
com base na estrutura de pastas e nomes de arquivos na pasta 'docs/'.

A ordem e a hierarquia são definidas por prefixos alfanuméricos
(ex: A1., a1.1, A2.a) e a exclusão de itens em revisão é feita por '#' inicial.
Inclui suporte para ícones Font Awesome usando a sintaxe [icon:nome-do-icone].

Autor: Fabio Takwara
Modificado por: Assistente IA
"""

import os
import yaml
import re

# --- Configurações ---
DOCS_DIR = 'docs'
MKDOCS_YML_PATH = 'mkdocs.yml'

# Regex para extrair: Prefixo, Ícone Opcional, Nome de Exibição
# Captura 1: ([a-zA-Z0-9\.]+) -> O prefixo (ex: A1., A2.a.)
# Captura 2: (?:\[icon:([^\]]+)\]\s*)? -> O ícone opcional (grupo não-capturante para o colchete e nome do ícone)
# Captura 3: (.*) -> O restante do nome como nome de exibição
ICON_NAME_REGEX = re.compile(r'^([a-zA-Z0-9\.]+)\s*(?:\[icon:([^\]]+)\])?\s*(.*)$')

# --- Funções Auxiliares ---

def parse_prefix_for_sort(prefix):
    """ Analisa um prefixo alfanumérico para ordenação. """
    parts = prefix.split('.')
    sort_key_parts = []
    for part in parts:
        if part.isdigit():
            sort_key_parts.append(int(part))
        else:
            sort_key_parts.append(part)
    return tuple(sort_key_parts)

def get_clean_name_and_path(entry_name, relative_dir_path):
    """
    Retorna o nome limpo (sem extensão) e o caminho relativo completo para um item.
    Ex: ('A1. Meu Artigo', '/A1. Meu Artigo')
    """
    name_without_ext = entry_name
    ext = ''
    # Processa apenas se tiver uma extensão conhecida para remover.
    if '.' in entry_name and entry_name.lower().endswith(('.md', '.txt', '.py')):
        name_without_ext, ext = os.path.splitext(entry_name)
        # ext = ext.lower() # Não precisamos mais da extensão em minúsculas aqui

    # Limpa espaços em branco extras no final do nome, se houver
    name_without_ext = name_without_ext.strip()

    # Monta o caminho relativo limpo, usando APENAS o nome sem extensão.
    # O caminho para o MkDocs geralmente não inclui a extensão .md
    clean_relative_path = os.path.join(relative_dir_path, name_without_ext).replace('\\', '/')
    return name_without_ext, clean_relative_path

def build_nav_structure(current_dir_full_path, current_dir_relative_path):
    temp_items = []
    try:
        entries = os.listdir(current_dir_full_path)
    except FileNotFoundError:
        print(f"Aviso: Diretório não encontrado: {current_dir_full_path}")
        return []

    for entry_name in entries:
        if entry_name.startswith('.') or entry_name.startswith('#'):
            continue

        entry_full_path = os.path.join(current_dir_full_path, entry_name)
        
        match = ICON_NAME_REGEX.match(entry_name)
        if not match:
            print(f"Aviso: Item '{entry_name}' não seguiu o padrão de prefixo/ícone esperado. Ignorando.")
            continue

        prefix = match.group(1)
        icon = match.group(2) # Pode ser None
        display_name_from_regex = match.group(3).strip() # Nome limpo especificado pelo usuário

        if not prefix:
            continue
            
        sort_key = parse_prefix_for_sort(prefix)
        
        is_dir = os.path.isdir(entry_full_path)
        
        # Determina o nome de exibição final: Usa o especificado na regex se houver, senão usa o nome do arquivo/pasta limpo.
        nome_exibicao_final = display_name_from_regex if display_name_from_regex else get_clean_name_and_path(entry_name, '')[0]
        
        if is_dir:
            sub_items_result = build_nav_structure(entry_full_path, os.path.join(current_dir_relative_path, entry_name).replace('\\', '/'))
            if sub_items_result:
                nav_item_dict_value = sub_items_result
                if icon:
                    nav_item_dict_value = {'icon': icon, 'children': sub_items_result}
                
                temp_items.append((sort_key, {nome_exibicao_final: nav_item_dict_value}))
        
        # Processa arquivos Markdown
        elif entry_name.lower().endswith('.md'): 
            # 1. Obtém o nome limpo apenas do nome do arquivo (sem extensão)
            clean_name_only, _ = get_clean_name_and_path(entry_name, '') 
            
            # 2. Constrói o caminho relativo do link usando APENAS o nome limpo
            item_link_path = os.path.join(current_dir_relative_path, clean_name_only).replace('\\', '/')

            if icon:
                item_config = {'icon': icon, 'link': item_link_path}
            else:
                item_config = item_link_path
            
            temp_items.append((sort_key, {nome_exibicao_final: item_config}))

    sorted_temp_items = sorted(temp_items, key=lambda item: item[0])
    nav_items = [item[1] for item in sorted_temp_items]
    return nav_items

# --- Execução Principal ---

if __name__ == "__main__":
    if not os.path.isdir(DOCS_DIR):
        print(f"Erro: Diretório '{DOCS_DIR}' não encontrado na raiz do repositório.")
        exit(1)

    print(f"Construindo estrutura de navegação a partir de '{DOCS_DIR}'...")
    nav_structure = build_nav_structure(DOCS_DIR, '') 

    if not nav_structure:
        print("Aviso: Nenhuma estrutura de navegação foi gerada. Verifique a pasta 'docs/' e os nomes dos arquivos/pastas.")
        exit(0)

    try:
        with open(MKDOCS_YML_PATH, 'r', encoding='utf-8') as f:
            mkdocs_config = yaml.safe_load(f)
            if mkdocs_config is None:
                mkdocs_config = {}
    except FileNotFoundError:
        print(f"Erro: Arquivo '{MKDOCS_YML_PATH}' não encontrado na raiz do repositório.")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Erro ao analisar o arquivo '{MKDOCS_YML_PATH}': {e}")
        exit(1)

    mkdocs_config['nav'] = nav_structure

    try:
        with open(MKDOCS_YML_PATH, 'w', encoding='utf-8') as f:
            yaml.safe_dump(mkdocs_config, f, default_flow_style=False, indent=2, allow_unicode=True)
        print(f"Seção 'nav:' atualizada com sucesso em '{MKDOCS_YML_PATH}'.")
        print("Agora você pode executar 'mkdocs serve' para ver as mudanças localmente ou 'mkdocs gh-deploy' para publicar.")
    except IOError as e:
        print(f"Erro ao escrever no arquivo '{MKDOCS_YML_PATH}': {e}")
        exit(1)