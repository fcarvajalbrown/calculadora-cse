"""
Cálculo del Índice de Necesidades (IN)
"""

import math
from constants import FACTOR_ESCALA
from calculator.coefficients import obtener_rango_edad, COEFICIENTES


def calcular_indice_necesidades(integrantes):
    """
    Calcula el Índice de Necesidades (IN).
    IN = N^0.7 + Y1 + Y2 + ... + Yn
    
    Args:
        integrantes: Lista de diccionarios con datos de cada integrante
        
    Returns:
        float: Índice de necesidades del hogar
    """
    n = len(integrantes)
    n_elevado = math.pow(n, FACTOR_ESCALA)

    suma_coeficientes = 0
    for integ in integrantes:
        rango = obtener_rango_edad(integ["edad"])
        condicion = integ["condicion"]
        coef = COEFICIENTES[rango].get(condicion, 0.0)
        suma_coeficientes += coef

    return n_elevado + suma_coeficientes


def calcular_ingreso_corregido(ingreso_equivalente, indice_necesidades):
    """
    Calcula el ingreso equivalente corregido.
    
    Args:
        ingreso_equivalente: Ingreso equivalente del hogar
        indice_necesidades: Índice de necesidades calculado
        
    Returns:
        float: Ingreso equivalente corregido
    """
    if indice_necesidades == 0:
        return 0
    return ingreso_equivalente / indice_necesidades