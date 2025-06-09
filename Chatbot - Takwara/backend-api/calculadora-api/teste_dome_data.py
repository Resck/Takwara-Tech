# test_dome_data.py
import functions_framework
from flask import jsonify

DOME_DATA = {
    "Icosahedron": { # Sólido Base: Icosaedro
        "V1": { # Frequência V1
            "truncation": {
                "2/3": { # No documento, V1 é referida como 2/3 esfera 
                    "segments": {"A": 1.05146}, # Coeficiente para o raio 
                    "num_segments": {"A": 25}, # Quantidade 
                    "vertex_angles": {"A": 31.72} # Ângulo de Dobra 
                }
            }
        },
        "V2": { # Frequência V2
            "truncation": {
                "1/2": { # Hemisfério 
                    "segments": {"A": 0.54653, "B": 0.61803}, # Coeficientes 
                    "num_segments": {"A": 30, "B": 35}, # Quantidades 
                    "vertex_angles": {"A": 15.86, "B": 18.00} # Ângulos de Dobra 
                }
            }
        },
        "V3": { # Frequência V3
            "truncation": {
                "3/8": { # Perfil Baixo (4/9) 
                    "segments": {"A": 0.34862, "B": 0.40355, "C": 0.41241}, # Coeficientes 
                    "num_segments": {"A": 30, "B": 40, "C": 50}, # Quantidades 
                    "vertex_angles": {"A": 10.04, "B": 11.64, "C": 11.90} # Ângulos de Dobra 
                },
                "5/8": { # Perfil Alto (5/9) 
                    "segments": {"A": 0.34862, "B": 0.40355, "C": 0.41241}, # Coeficientes 
                    "num_segments": {"A": 30, "B": 55, "C": 80}, # Quantidades 
                    "vertex_angles": {"A": 10.04, "B": 11.64, "C": 11.90} # Ângulos de Dobra 
                }
            }
        },
        "V4": { # Frequência V4
            "truncation": {
                "1/2": { # Hemisfério 
                    "segments": {"A": 0.25318, "B": 0.29453, "C": 0.29524, "D": 0.29859, "E": 0.31287, "F": 0.32492}, # Coeficientes 
                    "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 70, "F": 30}, # Quantidades 
                    "vertex_angles": {"A": 7.27, "B": 8.47, "C": 8.49, "D": 8.59, "E": 9.00, "F": 9.35} # Ângulos 
                }
            }
        },
        "L3": { # Variante L3 da V4 
            "truncation": {
                "1/2": { # Hemisfério 
                    "segments": {"A": 0.27590, "B": 0.28547, "C": 0.31287, "D": 0.32124, "E": 0.32492}, # Coeficientes 
                    "num_segments": {"A": 60, "B": 60, "C": 70, "D": 30, "E": 30}, # Quantidades 
                    "vertex_angles": {"A": 7.93, "B": 8.21, "C": 9.00, "D": 9.24, "E": 9.35} # Ângulos 
                }
            }
        },
        "V5": { # Frequência V5
            "truncation": {
                "7/15": { # Perfil mais baixo 
                    "segments": {"A": 0.19815, "B": 0.22569, "C": 0.23160, "D": 0.23179, "E": 0.24509, "F": 0.24535, "G": 0.24724, "H": 0.25517, "I": 0.26160}, # Coeficientes 
                    "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 50, "F": 10, "G": 60, "H": 50, "I": 30}, # Quantidades 
                    "vertex_angles": {"A": 5.69, "B": 6.48, "C": 6.65, "D": 6.66, "E": 7.04, "F": 7.05, "G": 7.10, "H": 7.33, "I": 7.52} # Ângulos 
                },
                "8/15": { # Perfil mais alto 
                    "segments": {"A": 0.19815, "B": 0.22569, "C": 0.23160, "D": 0.23179, "E": 0.24509, "F": 0.24535, "G": 0.24724, "H": 0.25517, "I": 0.26160}, # Coeficientes 
                    "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 80, "F": 20, "G": 70, "H": 70, "I": 35}, # Quantidades 
                    "vertex_angles": {"A": 5.69, "B": 6.48, "C": 6.65, "D": 6.66, "E": 7.04, "F": 7.05, "G": 7.10, "H": 7.33, "I": 7.52} # Ângulos 
                }
            }
        },
        "V6": { # Frequência V6
            "truncation": {
                "1/2": { # Hemisfério 
                    "segments": {"A": 0.16257, "B": 0.18191, "C": 0.18738, "D": 0.19048, "E": 0.19801, "F": 0.20282, "G": 0.20591, "H": 0.21535, "I": 0.21663}, # Coeficientes 
                    "num_segments": {"A": 30, "B": 60, "C": 30, "D": 30, "E": 60, "F": 90, "G": 130, "H": 65, "I": 60}, # Quantidades 
                    "vertex_angles": {"A": 4.66, "B": 5.22, "C": 5.38, "D": 5.47, "E": 5.68, "F": 5.82, "G": 5.91, "H": 6.18, "I": 6.22} # Ângulos 
                }
            }
        },
        "2V.3V": { # Variante 2V.3V da V6 (concatenada)
            "truncation": {
                "1/2": { # Hemisfério 
                    "segments": {"A": 0.18212, "B": 0.18854, "C": 0.18922, "D": 0.18932, "E": 0.19125, "F": 0.20591, "G": 0.21321, "H": 0.21445, "I": 0.21535, "J": 0.21663}, # Coeficientes 
                    "num_segments": {"A": 60, "B": 30, "C": 60, "D": 60, "E": 60, "F": 70, "G": 30, "H": 60, "I": 65, "J": 60}, # Quantidades 
                    "vertex_angles": {"A": 5.22, "B": 5.41, "C": 5.43, "D": 5.43, "E": 5.49, "F": 5.91, "G": 6.12, "H": 6.16, "I": 6.18, "J": 6.22} # Ângulos 
                }
            }
        }
    },
    "Cube": { # Sólido Base: Cubo
        "V1": { # V1 Cubo - Dados gerais disponíveis, mas não detalhados 
            "truncation": {
                "N/D": { # Truncagem não especificada no documento para V1-V4
                    "segments": {"A": "N/D"}, # Não disponível 
                    "num_segments": {"Total": 21}, # Total de Varetas 
                    "vertex_angles": {"N/D": "N/D"} # Não disponível
                }
            }
        },
        "V2": { # V2 Cubo - Dados gerais disponíveis, mas não detalhados 
            "truncation": {
                "N/D": {
                    "segments": {"A": "N/D"},
                    "num_segments": {"Total": 78}, # Total de Varetas 
                    "vertex_angles": {"N/D": "N/D"}
                }
            }
        },
        "V3": { # V3 Cubo - Dados gerais disponíveis, mas não detalhados 
            "truncation": {
                "N/D": {
                    "segments": {"A": "N/D"},
                    "num_segments": {"Total": 171}, # Total de Varetas 
                    "vertex_angles": {"N/D": "N/D"}
                }
            }
        },
        "V4": { # V4 Cubo - Dados gerais disponíveis, mas não detalhados 
            "truncation": {
                "N/D": {
                    "segments": {"A": "N/D"},
                    "num_segments": {"Total": 300}, # Total de Varetas 
                    "vertex_angles": {"N/D": "N/D"}
                }
            }
        },
        "V5": { # V5 Cubo - Dados detalhados disponíveis 
            "truncation": {
                "~1/2": { # Aproximadamente hemisférico 
                    "segments": { # Coeficientes 
                        "A": 0.17629, "B": 0.19100, "C": 0.19686, "D": 0.19765, "E": 0.20103,
                        "F": 0.20327, "G": 0.20588, "H": 0.21382, "I": 0.21400, "J": 0.21992,
                        "K": 0.22028, "L": 0.22264, "M": 0.22437, "N": 0.24051, "O": 0.24834,
                        "P": 0.25832, "Q": 0.26002, "R": 0.26089, "S": 0.27779, "T": 0.27793,
                        "U": 0.28006
                    },
                    "num_segments": { # Quantidades 
                        "A": 28, "B": 24, "C": 24, "D": 28, "E": 24, "F": 24, "G": 38, "H": 14,
                        "I": 24, "J": 24, "K": 24, "L": 24, "M": 24, "N": 24, "O": 12, "P": 24,
                        "Q": 14, "R": 24, "S": 24, "T": 12, "U": 7
                    },
                    "vertex_angles": { # Ângulos 
                        "A": 5.06, "B": 5.48, "C": 5.65, "D": 5.67, "E": 5.77, "F": 5.83,
                        "G": 5.91, "H": 6.14, "I": 6.14, "J": 6.31, "K": 6.32, "L": 6.39,
                        "M": 6.44, "N": 6.91, "O": 7.13, "P": 7.42, "Q": 7.47, "R": 7.50,
                        "S": 7.98, "T": 7.99, "U": 8.05
                    }
                }
            }
        },
        "V6": { # V6 Cubo - Dados detalhados disponíveis 
            "truncation": {
                "1/2": { # Hemisfério 
                    "segments": { # Coeficientes (A-AC, 29 tipos) 
                        "A": 0.14523, "B": 0.15547, "C": "N/D", "D": "N/D", "E": "N/D", "F": "N/D", "G": "N/D", "H": "N/D", "I": "N/D", "J": "N/D", "K": "N/D", "L": "N/D", "M": "N/D", "N": "N/D", "O": "N/D", "P": "N/D", "Q": "N/D", "R": "N/D", "S": "N/D", "T": "N/D", "U": "N/D", "V": "N/D", "W": "N/D", "X": "N/D", "Y": "N/D", "Z": "N/D", "AA": "N/D", "AB": "N/D", "AC": "N/D"
                    },
                    "num_segments": { # Quantidades (A-AC, 29 tipos) 
                        "A": 28, "B": 24, "C": "N/D", "D": "N/D", "E": "N/D", "F": "N/D", "G": "N/D", "H": "N/D", "I": "N/D", "J": "N/D", "K": "N/D", "L": "N/D", "M": "N/D", "N": "N/D", "O": "N/D", "P": "N/D", "Q": "N/D", "R": "N/D", "S": "N/D", "T": "N/D", "U": "N/D", "V": "N/D", "W": "N/D", "X": "N/D", "Y": "N/D", "Z": "N/D", "AA": "N/D", "AB": "N/D", "AC": "N/D"
                    },
                    "vertex_angles": { # Ângulos (A-AC, 29 tipos) 
                        "A": 4.16, "B": 4.46, "C": "N/D", "D": "N/D", "E": "N/D", "F": "N/D", "G": "N/D", "H": "N/D", "I": "N/D", "J": "N/D", "K": "N/D", "L": "N/D", "M": "N/D", "N": "N/D", "O": "N/D", "P": "N/D", "Q": "N/D", "R": "N/D", "S": "N/D", "T": "N/D", "U": "N/D", "V": "N/D", "W": "N/D", "X": "N/D", "Y": "N/D", "Z": "N/D", "AA": "N/D", "AB": "N/D", "AC": "N/D"
                    }
                }
            }
        },
        "2V.3V": { # Variante 2V.3V da V6 (concatenada) 
            "truncation": {
                "1/2": { # Hemisfério 
                    "segments": { # Coeficientes (A-AA, 27 tipos) 
                        "A": 0.15768, "B": 0.16179, "C": "N/D", "D": "N/D", "E": "N/D", "F": "N/D", "G": "N/D", "H": "N/D", "I": "N/D", "J": "N/D", "K": "N/D", "L": "N/D", "M": "N/D", "N": "N/D", "O": "N/D", "P": "N/D", "Q": "N/D", "R": "N/D", "S": "N/D", "T": "N/D", "U": "N/D", "V": "N/D", "W": "N/D", "X": "N/D", "Y": "N/D", "Z": "N/D", "AA": "N/D"
                    },
                    "num_segments": { # Quantidades (A-AA, 27 tipos) 
                        "A": 56, "B": 28, "C": "N/D", "D": "N/D", "E": "N/D", "F": "N/D", "G": "N/D", "H": "N/D", "I": "N/D", "J": "N/D", "K": "N/D", "L": "N/D", "M": "N/D", "N": "N/D", "O": "N/D", "P": "N/D", "Q": "N/D", "R": "N/D", "S": "N/D", "T": "N/D", "U": "N/D", "V": "N/D", "W": "N/D", "X": "N/D", "Y": "N/D", "Z": "N/D", "AA": "N/D"
                    },
                    "vertex_angles": { # Ângulos (A-AA, 27 tipos) 
                        "A": 4.52, "B": 4.64, "C": "N/D", "D": "N/D", "E": "N/D", "F": "N/D", "G": "N/D", "H": "N/D", "I": "N/D", "J": "N/D", "K": "N/D", "L": "N/D", "M": "N/D", "N": "N/D", "O": "N/D", "P": "N/D", "Q": "N/D", "R": "N/D", "S": "N/D", "T": "N/D", "U": "N/D", "V": "N/D", "W": "N/D", "X": "N/D", "Y": "N/D", "Z": "N/D", "AA": "N/D"
                    }
                }
            }
        },
        "3V.2V": { # Variante 3V.2V da V6 (concatenada) 
            "truncation": {
                "1/2": { # Hemisfério 
                    "segments": { # Coeficientes (A-V, 22 tipos) 
                        "A": 0.15325, "B": 0.15508, "C": "N/D", "D": "N/D", "E": "N/D", "F": "N/D", "G": "N/D", "H": "N/D", "I": "N/D", "J": "N/D", "K": "N/D", "L": "N/D", "M": "N/D", "N": "N/D", "O": "N/D", "P": "N/D", "Q": "N/D", "R": "N/D", "S": "N/D", "T": "N/D", "U": "N/D", "V": "N/D"
                    },
                    "num_segments": { # Quantidades (A-V, 22 tipos) 
                        "A": 56, "B": 24, "C": "N/D", "D": "N/D", "E": "N/D", "F": "N/D", "G": "N/D", "H": "N/D", "I": "N/D", "J": "N/D", "K": "N/D", "L": "N/D", "M": "N/D", "N": "N/D", "O": "N/D", "P": "N/D", "Q": "N/D", "R": "N/D", "S": "N/D", "T": "N/D", "U": "N/D", "V": "N/D"
                    },
                    "vertex_angles": { # Ângulos (A-V, 22 tipos) 
                        "A": 4.39, "B": 4.45, "C": "N/D", "D": "N/D", "E": "N/D", "F": "N/D", "G": "N/D", "H": "N/D", "I": "N/D", "J": "N/D", "K": "N/D", "L": "N/D", "M": "N/D", "N": "N/D", "O": "N/D", "P": "N/D", "Q": "N/D", "R": "N/D", "S": "N/D", "T": "N/D", "U": "N/D", "V": "N/D"
                    }
                }
            }
        }
    },
    "Octahedron": { # Sólido Base: Octaedro
        "V1": { # V1 Octaedro
            "truncation": {
                "1/2": { # Hemisfério 
                    "segments": {"A": 1.41421}, # Coeficiente 
                    "num_segments": {"A": 8}, # Quantidade 
                    "vertex_angles": {"A": 45.00} # Ângulo 
                }
            }
        },
        "V2": { # V2 Octaedro 
            "truncation": {
                "1/2": { # Hemisfério 
                    "segments": {"A": 0.76537, "B": 1.00000}, # Coeficientes 
                    "num_segments": {"A": 16, "B": 12}, # Quantidades 
                    "vertex_angles": {"A": 22.50, "B": 30.00} # Ângulos 
                }
            }
        },
        "V3": { # V3 Octaedro 
            "truncation": {
                "1/2": { # Hemisfério 
                    "segments": {"A": 0.45951, "B": 0.63246, "C": 0.67142}, # Coeficientes 
                    "num_segments": {"A": 16, "B": 20, "C": 24}, # Quantidades 
                    "vertex_angles": {"A": 13.28, "B": 18.44, "C": 19.62} # Ângulos 
                }
            }
        },
        "L3_3/8": { # Octaedro L3 3/8 - Dados gerais disponíveis, mas não detalhados 
            "truncation": {
                "3/8": {
                    "segments": {"A": "N/D"}, # Não disponível 
                    "num_segments": {"Total": 60}, # Total de Varetas 
                    "vertex_angles": {"N/D": "N/D"} # Não disponível 
                }
            }
        },
        "L3_5/8": { # Octaedro L3 5/8 - Dados gerais disponíveis, mas não detalhados 
            "truncation": {
                "5/8": {
                    "segments": {"A": "N/D"}, # Não disponível 
                    "num_segments": {"Total": 144}, # Total de Varetas 
                    "vertex_angles": {"N/D": "N/D"} # Não disponível 
                }
            }
        },
        # As frequências V4, V5, V6 do Octaedro têm apenas informações gerais 
        "V4": {
            "truncation": {
                "N/D": {
                    "segments": {"A": "N/D"},
                    "num_segments": {"Total": 104}, # Total de Varetas 
                    "vertex_angles": {"N/D": "N/D"}
                }
            }
        },
        "V5": {
            "truncation": {
                "N/D": {
                    "segments": {"A": "N/D"},
                    "num_segments": {"Total": 160}, # Total de Varetas 
                    "vertex_angles": {"N/D": "N/D"}
                }
            }
        },
        "V6": {
            "truncation": {
                "N/D": {
                    "segments": {"A": "N/D"},
                    "num_segments": {"Total": 228}, # Total de Varetas 
                    "vertex_angles": {"N/D": "N/D"}
                }
            }
        },
    },
    "Dodecahedron": { # Sólido Base: Dodecaedro
        "L1": { # Variante L1 
            "truncation": {
                "N/D": { # Truncagem não especificada no documento para Dodecaedro L1/L2/L2T
                    "segments": {"A": 0.64085, "B": 0.71364}, # Coeficientes 
                    "num_segments": {"A": 60, "B": 30}, # Quantidades 
                    "vertex_angles": {"N/D": "N/D"} # Não fornecido explicitamente 
                }
            }
        },
        "L2": { # Variante L2 
            "truncation": {
                "N/D": {
                    "segments": {"A": 0.32474, "B": 0.34034, "C": 0.36284, "D": 0.37668}, # Coeficientes 
                    "num_segments": {"A": 120, "B": 120, "C": 60, "D": 60}, # Quantidades 
                    "vertex_angles": {"N/D": "N/D"} # Não fornecido explicitamente 
                }
            }
        },
        "L2T": { # Variante L2T (Triaconizada) 
            "truncation": {
                "N/D": {
                    "segments": { # Coeficientes (A-F, 6 tipos) 
                        "A": 0.19071, "B": 0.21151, "C": "N/D", "D": "N/D", "E": "N/D", "F": "N/D" # Os 4 tipos restantes não listados explicitamente no doc
                    },
                    "num_segments": { # Quantidades (A-F, 6 tipos) 
                        "A": 60, "B": 120, "C": "N/D", "D": "N/D", "E": "N/D", "F": "N/D" # Os 4 tipos restantes não listados explicitamente no doc
                    },
                    "vertex_angles": {"N/D": "N/D"} # Não fornecido explicitamente 
                }
            }
        }
    },
    "Tetrahedron": { # Sólido Base: Tetraedro
        "L2T": { # Variante L2T (Triaconizada) 
            "truncation": {
                "N/D": { # Truncagem não especificada
                    "segments": {"A": 0.91940, "B": 1.15470}, # Coeficientes 
                    "num_segments": {"A": 14, "B": 7}, # Quantidades 
                    "vertex_angles": {"N/D": "N/D"} # Não fornecido explicitamente 
                }
            }
        },
        "L3T": { # Variante L3T (Triaconizada) 
            "truncation": {
                "N/D": {
                    "segments": { # Coeficientes (A-F, 6 tipos) 
                        "A": 0.29239, "B": 0.35693, "C": 0.47313, "D": 0.48701, "E": 0.60581, "F": 0.66092
                    },
                    "num_segments": {"A": 12, "B": 24, "C": 28, "D": 12, "E": 14, "F": 24}, # Quantidades 
                    "vertex_angles": {"N/D": "N/D"} # Não fornecido explicitamente 
                }
            }
        }
    }
}

@functions_framework.http
def test_dome_data_api(request):
    # Apenas tenta acessar uma parte do DOME_DATA para verificar
    try:
        # Tente acessar um dado específico que você sabe que existe
        test_value = DOME_DATA["Icosahedron"]["V1"]["truncation"]["2/3"]["segments"]["A"]
        return jsonify({"success": True, "message": "DOME_DATA carregado com sucesso!", "test_value": test_value}), 200
    except Exception as e:
        # Se algo falhar, retorne o erro detalhado
        return jsonify({"success": False, "error": f"Erro ao carregar DOME_DATA: {str(e)}"}), 500