"""
Cálculo del ingreso equivalente del hogar
"""

from constants import SALARIO_MINIMO, UMBRALES_INGRESO


def calcular_ingreso_equivalente(integrantes):
    """
    Calcula el ingreso equivalente del hogar (suma de ingresos de mayores de 18).
    
    Args:
        integrantes: Lista de diccionarios con datos de cada integrante
        
    Returns:
        float: Ingreso equivalente total del hogar
    """
    total = 0
    
    for integ in integrantes:
        edad = integ["edad"]
        ing_trabajo = integ["ingreso_trabajo"]
        ing_pension = integ["ingreso_pension"]
        ing_capital = integ["ingreso_capital"]

        if edad < 18:
            # Se excluyen ingresos de menores de 18
            continue

        if 18 <= edad <= 24 and integ.get("estudia", False):
            # Persona entre 18-24 que estudia y trabaja:
            # solo se consideran ingresos si superan 2 salarios mínimos
            ingreso_total_persona = ing_trabajo + ing_pension + ing_capital
            umbral = 2 * SALARIO_MINIMO
            if ingreso_total_persona > umbral:
                total += ingreso_total_persona - umbral
        else:
            total += ing_trabajo + ing_pension + ing_capital

    return total


def determinar_tramo_por_ingreso(ingreso_corregido):
    """
    Determina el tramo de la CSE según el ingreso equivalente corregido.
    
    Args:
        ingreso_corregido: Ingreso equivalente corregido
        
    Returns:
        int: Tramo de la CSE (40, 50, 60, 70, 80, 90 o 100)
    """
    for umbral, tramo in UMBRALES_INGRESO:
        if ingreso_corregido <= umbral:
            return tramo
    return 100