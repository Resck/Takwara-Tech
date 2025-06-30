# /Users/fabiotakwara/Documents/GitHub/Takwara-Tech/Chatbot - Takwara/backend-api/calculadora-api/main.py

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