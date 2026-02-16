"""
Generador de reportes de resultados CSE
"""

import math
from constants import SALARIO_MINIMO, TRAMO_DESCRIPCIONES, FACTOR_ESCALA
from calculator.coefficients import obtener_rango_edad, COEFICIENTES


def generar_reporte(integrantes, ingreso_equiv, indice_nec, ingreso_corregido,
                   tramo_ingreso, tramo_medios, num_medios, detalle_medios):
    """
    Genera el reporte completo de resultados.
    
    Returns:
        str: Reporte formateado
    """
    tramo_final = max(tramo_ingreso, tramo_medios)
    
    lineas = []
    lineas.append("=" * 70)
    lineas.append("   RESULTADO - CALIFICACIÓN SOCIOECONÓMICA (CSE)")
    lineas.append("=" * 70)
    lineas.append("")

    # PASO 1: Ingreso equivalente
    lineas.extend(_seccion_ingreso_equivalente(integrantes, ingreso_equiv))

    # PASO 2: Índice de necesidades
    lineas.extend(_seccion_indice_necesidades(integrantes, indice_nec))

    # PASO 3: Ingreso corregido
    lineas.extend(_seccion_ingreso_corregido(ingreso_equiv, indice_nec, ingreso_corregido))

    # PASO 4: Tramo por ingresos
    lineas.extend(_seccion_tramo_ingreso(tramo_ingreso))

    # PASO 5: Test de medios
    lineas.extend(_seccion_test_medios(num_medios, detalle_medios, tramo_medios))

    # Resultado final
    lineas.extend(_seccion_resultado_final(tramo_final))

    return "\n".join(lineas)


def _seccion_ingreso_equivalente(integrantes, ingreso_equiv):
    """Genera la sección de ingreso equivalente."""
    lineas = []
    lineas.append("PASO 1: INGRESO EQUIVALENTE DEL HOGAR")
    lineas.append("-" * 50)
    
    for integ in integrantes:
        nombre = integ["nombre"]
        edad = integ["edad"]
        it = integ["ingreso_trabajo"]
        ip = integ["ingreso_pension"]
        ic = integ["ingreso_capital"]
        total_persona = it + ip + ic
        nota = ""
        
        if edad < 18:
            nota = " (excluido por ser menor de 18)"
        elif 18 <= edad <= 24 and integ.get("estudia", False):
            umbral = 2 * SALARIO_MINIMO
            if total_persona > umbral:
                nota = f" (estudia 18-24: se considera ${total_persona - umbral:,.0f})"
            else:
                nota = " (estudia 18-24: no supera 2 salarios mínimos, no se considera)"
        
        lineas.append(f"  {nombre} ({edad} años):")
        lineas.append(f"    Trabajo: ${it:>12,.0f}  |  Pensión: ${ip:>12,.0f}  |  Capital: ${ic:>12,.0f}{nota}")

    lineas.append(f"\n  >> Ingreso equivalente del hogar = ${ingreso_equiv:,.0f}")
    lineas.append("")
    return lineas


def _seccion_indice_necesidades(integrantes, indice_nec):
    """Genera la sección de índice de necesidades."""
    lineas = []
    lineas.append("PASO 2: ÍNDICE DE NECESIDADES (IN)")
    lineas.append("-" * 50)
    
    n = len(integrantes)
    n_exp = math.pow(n, FACTOR_ESCALA)
    lineas.append(f"  Número de integrantes (N): {n}")
    lineas.append(f"  N^0.7 = {n}^0.7 = {n_exp:.8f}")
    lineas.append("")
    
    suma_y = 0
    for integ in integrantes:
        rango = obtener_rango_edad(integ["edad"])
        coef = COEFICIENTES[rango].get(integ["condicion"], 0.0)
        suma_y += coef
        lineas.append(f"  {integ['nombre']} ({integ['edad']} años) - {integ['condicion']}")
        lineas.append(f"    Rango: {rango} | Coeficiente Y = {coef:.2f}")

    lineas.append(f"\n  IN = {n_exp:.8f} + {suma_y:.2f} = {indice_nec:.8f}")
    lineas.append(f"\n  >> Índice de necesidades = {indice_nec:.8f}")
    lineas.append("")
    return lineas


def _seccion_ingreso_corregido(ingreso_equiv, indice_nec, ingreso_corregido):
    """Genera la sección de ingreso corregido."""
    lineas = []
    lineas.append("PASO 3: INGRESO EQUIVALENTE CORREGIDO")
    lineas.append("-" * 50)
    lineas.append("  Ingreso equivalente / Índice de necesidades")
    lineas.append(f"  = ${ingreso_equiv:,.0f} / {indice_nec:.8f}")
    lineas.append(f"\n  >> Ingreso equivalente corregido = ${ingreso_corregido:,.0f}")
    lineas.append("")
    return lineas


def _seccion_tramo_ingreso(tramo_ingreso):
    """Genera la sección de tramo por ingresos."""
    lineas = []
    lineas.append("PASO 4: TRAMO POR INGRESOS")
    lineas.append("-" * 50)
    lineas.append(f"  >> Tramo inicial por ingresos = {tramo_ingreso}% de la CSE")
    lineas.append("")
    return lineas


def _seccion_test_medios(num_medios, detalle_medios, tramo_medios):
    """Genera la sección de test de medios."""
    lineas = []
    lineas.append("PASO 5: TEST DE MEDIOS (FACTORES DE REORDENAMIENTO)")
    lineas.append("-" * 50)
    
    if num_medios == 0:
        lineas.append("  No se activaron test de medios.")
    else:
        lineas.append(f"  Medios activos: {num_medios}")
        for d in detalle_medios:
            lineas.append(f"    - {d}")
        lineas.append(f"\n  >> Tramo inferido por test de medios = {tramo_medios}% de la CSE")
    
    lineas.append("")
    return lineas


def _seccion_resultado_final(tramo_final):
    """Genera la sección de resultado final."""
    lineas = []
    lineas.append("=" * 70)
    lineas.append(f"  TRAMO FINAL DE LA CSE: {tramo_final}%")
    lineas.append("=" * 70)
    lineas.append("")

    # Descripción del tramo
    if tramo_final <= 70:
        desc = "Menores ingresos y mayor vulnerabilidad"
    else:
        desc = "Mayores ingresos y menor vulnerabilidad"
    lineas.append(f"  Clasificación: {desc}")
    lineas.append(f"  {TRAMO_DESCRIPCIONES.get(tramo_final, '')}")
    
    return lineas