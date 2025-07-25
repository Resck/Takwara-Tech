# -*- coding: utf-8 -*-
"""
Script final para gerar a navegação, tratando o index.md de forma especial.
"""
import os
import yaml
import re
from typing import List, Dict, Any, Tuple, Optional

# --- Configurações Simplificadas ---
DOCS_DIR = 'docs'
MKDOCS_YML_PATH = 'mkdocs.yml'

# --- Funções Auxiliares ---

def extract_prefix_and_name(entry_name: str) -> Tuple[Optional[str], str]:
    match = re.match(r'^([a-zA-Z0-9\.]+)\s+(.*)', entry_name)
    if match: return match.group(1), match.group(2)
    return None, entry_name

def parse_prefix_for_sort(prefix: str) -> Tuple:
    parts = prefix.split('.')
    sort_key_parts = []
    for part in parts:
        if part.isdigit():
            sort_key_parts.append(part.zfill(8))
        else:
            sub_parts = re.findall(r'(\d+|\D+)', part)
            for sub_part in sub_parts:
                if sub_part.isdigit():
                    sort_key_parts.append(sub_part.zfill(8))
                else:
                    sort_key_parts.append(sub_part)
    return tuple(sort_key_parts)

def get_display_name(raw_name: str) -> str:
    name, ext = os.path.splitext(raw_name)
    if ext.lower() in ['.md', '.pdf']: return name
    return raw_name

def build_nav_structure(current_dir: str, relative_path: str = '') -> List[Dict[str, Any]]:
    items_to_sort = []
    home_item = None # Variável para guardar o item da página inicial

    try:
        entries = os.listdir(current_dir)
    except FileNotFoundError:
        return []

    for entry_name in entries:
        # --- LÓGICA NOVA: Tratar o index.md separadamente ---
        if entry_name.lower() == 'index.md' and relative_path == '':
            home_item = {'Bem vind@!': 'index.md'}
            continue # Pula para o próximo ficheiro

        if entry_name.startswith('.') or entry_name.startswith('#') or entry_name == 'assets':
            continue

        full_path = os.path.join(current_dir, entry_name)
        is_dir = os.path.isdir(full_path)

        if not is_dir and not (entry_name.lower().endswith('.md') or entry_name.lower().endswith('.pdf')):
            continue

        prefix, raw_name = extract_prefix_and_name(entry_name)
        display_name = get_display_name(raw_name)

        if is_dir and not display_name:
            display_name = get_display_name(entry_name)

        sort_key: Tuple
        if prefix:
            sort_key = parse_prefix_for_sort(prefix)
        else:
            sort_key = ('~', entry_name)

        nav_item = None
        if is_dir:
            sub_nav = build_nav_structure(full_path, os.path.join(relative_path, entry_name))
            if sub_nav:
                nav_item = {display_name: sub_nav}
        else:
            link_path = os.path.join(relative_path, entry_name)
            link_path = link_path.replace('\\', '/')
            nav_item = {display_name: link_path}

        if nav_item:
            items_to_sort.append((sort_key, nav_item))

    items_to_sort.sort(key=lambda x: x[0])
    
    # Constrói a lista final, colocando o home_item no início
    final_nav = []
    if home_item:
        final_nav.append(home_item)
    
    final_nav.extend([item[1] for item in items_to_sort])
    
    return final_nav

# --- Execução Principal ---
if __name__ == "__main__":
    if not os.path.isdir(DOCS_DIR):
        print(f"ERRO: Diretório '{DOCS_DIR}' não encontrado.")
        exit(1)

    try:
        with open(MKDOCS_YML_PATH, 'r', encoding='utf-8') as f:
            mkdocs_config = yaml.safe_load(f) or {}
    except FileNotFoundError:
        mkdocs_config = {}

    print("Gerando estrutura de navegação...")
    nav_structure = build_nav_structure(DOCS_DIR, '')

    if not nav_structure:
        print("AVISO: Nenhuma estrutura de navegação foi gerada.")
        exit(0)

    mkdocs_config['nav'] = nav_structure

    try:
        with open(MKDOCS_YML_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(mkdocs_config, f, default_flow_style=False, sort_keys=False, indent=2, allow_unicode=True)
        print(f"SUCESSO: Seção 'nav' atualizada em '{MKDOCS_YML_PATH}'.")
    except IOError as e:
        print(f"ERRO ao escrever no arquivo '{MKDOCS_YML_PATH}': {e}")
        exit(1)