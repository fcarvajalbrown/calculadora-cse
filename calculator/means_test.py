"""
Evaluación de test de medios (factores de reordenamiento)
"""


def evaluar_test_medios(datos_medios):
    """
    Evalúa los test de medios y retorna el tramo inferido más alto.
    
    Args:
        datos_medios: Diccionario con flags booleanos de cada test
        
    Returns:
        tuple: (tramo_inferido, total_medios, detalle)
    """
    medios_activos_alto = []
    medios_activos_muy_alto = []
    detalle = []

    # 1. Cotización de salud
    if datos_medios.get("salud_alto_valor", False):
        medios_activos_alto.append("salud")
        detalle.append("Cotización de salud: Plan de alto valor -> Tramo 50")
    if datos_medios.get("salud_muy_alto_valor", False):
        medios_activos_muy_alto.append("salud")
        detalle.append("Cotización de salud: Plan de muy alto valor -> Tramo 90")

    # 2. Matrícula educacional de alto valor (>= $100.000)
    if datos_medios.get("educacion_alto_valor", False):
        medios_activos_alto.append("educacion")
        detalle.append("Matrícula educacional de alto valor (>= $100.000)")

    # 3. Vehículos terrestres y/o embarcaciones
    if datos_medios.get("vehiculos_alto_valor", False):
        medios_activos_alto.append("vehiculos")
        detalle.append("Vehículos: Alto valor (>= 20% más costosos) -> Tramo 50")
    if datos_medios.get("vehiculos_muy_alto_valor", False):
        medios_activos_muy_alto.append("vehiculos")
        detalle.append("Vehículos: Muy alto valor (>= 5% más costosos) -> Tramo 90")
    if datos_medios.get("nave_mayor", False):
        medios_activos_muy_alto.append("nave_mayor")
        detalle.append("Nave mayor -> Tramo 90")
    if datos_medios.get("tres_naves_menores", False):
        medios_activos_muy_alto.append("naves_menores")
        detalle.append("3 o más naves menores/deportivas -> Tramo 90")

    # 4. Bienes raíces
    if datos_medios.get("bienes_raices_alto_valor", False):
        medios_activos_alto.append("bienes_raices")
        detalle.append("Bienes raíces: Alto valor (>= 20% más costosos) -> Se activa con otro medio")
    if datos_medios.get("bienes_raices_muy_alto_valor", False):
        medios_activos_muy_alto.append("bienes_raices")
        detalle.append("Bienes raíces: Muy alto valor (>= 5% más costosos) -> Tramo 90")

    # 5. Ingresos padre/madre no presente
    if datos_medios.get("padre_madre_alto_valor", False):
        medios_activos_alto.append("padre_madre")
        detalle.append("Ingresos padre/madre no presente: Alto valor -> Tramo 80")
    if datos_medios.get("padre_madre_muy_alto_valor", False):
        medios_activos_muy_alto.append("padre_madre")
        detalle.append("Ingresos padre/madre no presente: Muy alto valor -> Tramo 90")

    total_medios_alto = len(medios_activos_alto)
    total_medios_muy_alto = len(medios_activos_muy_alto)

    tramo_inferido = 0

    # Determinar tramo por medios individuales de muy alto valor
    if total_medios_muy_alto >= 1:
        tramo_inferido = 90

    # Regla: 2+ medios de muy alto valor => tramo 100
    if total_medios_muy_alto >= 2:
        tramo_inferido = 100

    # Si no hay muy alto valor, evaluar alto valor
    if tramo_inferido == 0:
        # Medios individuales de alto valor
        tramos_alto = []
        if "salud" in medios_activos_alto:
            tramos_alto.append(50)
        if "vehiculos" in medios_activos_alto:
            tramos_alto.append(50)
        if "padre_madre" in medios_activos_alto:
            tramos_alto.append(80)
        # educacion y bienes_raices solo se activan en presencia de otro medio
        if "educacion" in medios_activos_alto and total_medios_alto >= 2:
            tramos_alto.append(50)
        if "bienes_raices" in medios_activos_alto and total_medios_alto >= 2:
            tramos_alto.append(50)

        if tramos_alto:
            tramo_inferido = max(tramos_alto)

        # Regla: 2+ medios de alto valor y ambos < 70 => tramo 70
        if total_medios_alto >= 2 and tramo_inferido < 70:
            tramo_inferido = 70

        # Regla: 3+ medios de alto valor => tramo 90
        if total_medios_alto >= 3:
            tramo_inferido = 90

    total_medios = total_medios_alto + total_medios_muy_alto
    return tramo_inferido, total_medios, detalle