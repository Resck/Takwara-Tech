# calculadora-api/main.py - VERSÃO FINAL E CORRIGIDA

import functions_framework
from flask import jsonify
import math

# SUA BASE DE DADOS COMPLETA, COM A SINTAXE CORRIGIDA
DOME_DATA = {
    "Icosahedron": {
        "V1": {"truncation": {"2/3": {"segments": {"A": 1.05146}, "num_segments": {"A": 25}, "vertex_angles": {"A": 31.72}}}},
        "V2": {"truncation": {"1/2": {"segments": {"A": 0.54653, "B": 0.61803}, "num_segments": {"A": 30, "B": 35}, "vertex_angles": {"A": 15.86, "B": 18.00}}}},
        "V3": {"truncation": {
            "3/8": {"segments": {"A": 0.34862, "B": 0.40355, "C": 0.41241}, "num_segments": {"A": 30, "B": 40, "C": 50}, "vertex_angles": {"A": 10.04, "B": 11.64, "C": 11.90}},
            "5/8": {"segments": {"A": 0.34862, "B": 0.40355, "C": 0.41241}, "num_segments": {"A": 30, "B": 55, "C": 80}, "vertex_angles": {"A": 10.04, "B": 11.64, "C": 11.90}}
        }},
        "V4": {"truncation": {"1/2": {"segments": {"A": 0.25318, "B": 0.29453, "C": 0.29524, "D": 0.29859, "E": 0.31287, "F": 0.32492}, "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 70, "F": 30}, "vertex_angles": {"A": 7.27, "B": 8.47, "C": 8.49, "D": 8.59, "E": 9.00, "F": 9.35}}}},
        "L3": {"truncation": {"1/2": {"segments": {"A": 0.27590, "B": 0.28547, "C": 0.31287, "D": 0.32124, "E": 0.32492}, "num_segments": {"A": 60, "B": 60, "C": 70, "D": 30, "E": 30}, "vertex_angles": {"A": 7.93, "B": 8.21, "C": 9.00, "D": 9.24, "E": 9.35}}}},
        "V5": {"truncation": {
            "7/15": {"segments": {"A": 0.19815, "B": 0.22569, "C": 0.23160, "D": 0.23179, "E": 0.24509, "F": 0.24535, "G": 0.24724, "H": 0.25517, "I": 0.26160}, "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 50, "F": 10, "G": 60, "H": 50, "I": 30}, "vertex_angles": {"A": 5.69, "B": 6.48, "C": 6.65, "D": 6.66, "E": 7.04, "F": 7.05, "G": 7.10, "H": 7.33, "I": 7.52}},
            "8/15": {"segments": {"A": 0.19815, "B": 0.22569, "C": 0.23160, "D": 0.23179, "E": 0.24509, "F": 0.24535, "G": 0.24724, "H": 0.25517, "I": 0.26160}, "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 80, "F": 20, "G": 70, "H": 70, "I": 35}, "vertex_angles": {"A": 5.69, "B": 6.48, "C": 6.65, "D": 6.66, "E": 7.04, "F": 7.05, "G": 7.10, "H": 7.33, "I": 7.52}}
        }},
        "V6": {"truncation": {"1/2": {"segments": {"A": 0.16257, "B": 0.18191, "C": 0.18738, "D": 0.19048, "E": 0.19801, "F": 0.20282, "G": 0.20591, "H": 0.21535, "I": 0.21663}, "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 60, "F": 90, "G": 130, "H": 65, "I": 60}, "vertex_angles": {"A": 4.66, "B": 5.22, "C": 5.38, "D": 5.47, "E": 5.68, "F": 5.82, "G": 5.91, "H": 6.18, "I": 6.22}}}},
        "2V.3V": {"truncation": {"1/2": {"segments": {"A": 0.18212, "B": 0.18854, "C": 0.18922, "D": 0.18932, "E": 0.19125, "F": 0.20591, "G": 0.21321, "H": 0.21445, "I": 0.21535, "J": 0.21663}, "num_segments": {"A": 60, "B": 30, "C": 60, "D": 60, "E": 60, "F": 70, "G": 30, "H": 60, "I": 65, "J": 60}, "vertex_angles": {"A": 5.22, "B": 5.41, "C": 5.43, "D": 5.43, "E": 5.49, "F": 5.91, "G": 6.12, "H": 6.16, "I": 6.18, "J": 6.22}}}},
    },
    "Cube": {
        "V5": {"truncation": {"~1/2": {"segments": {"A": 0.17629, "B": 0.19100, "C": 0.19686, "D": 0.19765, "E": 0.20103, "F": 0.20327, "G": 0.20588, "H": 0.21382, "I": 0.21400, "J": 0.21992, "K": 0.22028, "L": 0.22264, "M": 0.22437, "N": 0.24051, "O": 0.24834, "P": 0.25832, "Q": 0.26002, "R": 0.26089, "S": 0.27779, "T": 0.27793, "U": 0.28006}, "num_segments": {"A": 28, "B": 24, "C": 24, "D": 28, "E": 24, "F": 24, "G": 38, "H": 14, "I": 24, "J": 24, "K": 24, "L": 24, "M": 24, "N": 24, "O": 12, "P": 24, "Q": 14, "R": 24, "S": 24, "T": 12, "U": 7}, "vertex_angles": {"A": 5.06, "B": 5.48, "C": 5.65, "D": 5.67, "E": 5.77, "F": 5.83, "G": 5.91, "H": 6.14, "I": 6.14, "J": 6.31, "K": 6.32, "L": 6.39, "M": 6.44, "N": 6.91, "O": 7.13, "P": 7.42, "Q": 7.47, "R": 7.50, "S": 7.98, "T": 7.99, "U": 8.05}}}}
    },
    "Octahedron": {
        "V1": {"truncation": {"1/2": {"segments": {"A": 1.41421}, "num_segments": {"A": 8}, "vertex_angles": {"A": 45.00}}}},
        "V2": {"truncation": {"1/2": {"segments": {"A": 0.76537, "B": 1.00000}, "num_segments": {"A": 16, "B": 12}, "vertex_angles": {"A": 22.50, "B": 30.00}}}},
        "V3": {"truncation": {"1/2": {"segments": {"A": 0.45951, "B": 0.63246, "C": 0.67142}, "num_segments": {"A": 16, "B": 20, "C": 24}, "vertex_angles": {"A": 13.28, "B": 18.44, "C": 19.62}}}}
    },
    "Dodecahedron": {
        "L1": {"truncation": {"N/D": {"segments": {"A": 0.64085, "B": 0.71364}, "num_segments": {"A": 60, "B": 30}, "vertex_angles": {"N/D": "N/D"}}}}
    },
    "Tetrahedron": {
        "L2T": {"truncation": {"N/D": {"segments": {"A": 0.91940, "B": 1.15470}, "num_segments": {"A": 14, "B": 7}, "vertex_angles": {"N/D": "N/D"}}}}
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

        dome_info = DOME_DATA[base_solid][frequency]['truncation'][truncation]
        
        radius = diameter / 2.0
        calculated_lengths = {
            key: f"{radius * coeff:.4f}" if isinstance(coeff, (int, float)) else coeff
            for key, coeff in dome_info['segments'].items()
        }

        results = {
            "success": True,
            "segment_lengths": calculated_lengths,
            "num_segments": dome_info['num_segments'],
            "vertex_angles": dome_info['vertex_angles']
        }
        response = jsonify(results)

    except (ValueError, TypeError) as e:
        response = jsonify({"success": False, "error": f"Erro nos dados de entrada ou cálculo: {str(e)}"})
    
    except KeyError as e:
        response = jsonify({"success": False, "error": f"Combinação de Sólido/Frequência/Truncagem não encontrada. Chave ausente: {e}."})
    
    except Exception as e:
        response = jsonify({"success": False, "error": f"Ocorreu um erro inesperado no servidor: {str(e)}"})

    for header, value in headers.items():
        response.headers[header] = value
    return response