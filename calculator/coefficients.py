"""
Tabla de coeficientes según edad y condición
Basado en Tabla N°1 - Resolución Exenta N°082
"""

COEFICIENTES = {
    "0-5": {
        "Sin discapacidad, dependencia o NEE": 0.40,
        "Con discapacidad, dependencia o NEE": 0.80,
    },
    "6-14": {
        "Sin discapacidad, dependencia o NEE": 0.30,
        "Discapacidad Leve": 0.34,
        "Discapacidad o dependencia moderada": 0.52,
        "Discapacidad o dependencia severa/profunda o NEE": 0.64,
    },
    "15-17": {
        "Sin discapacidad, dependencia o NEE": 0.09,
        "Discapacidad Leve": 0.34,
        "Discapacidad o dependencia moderada": 0.52,
        "Discapacidad o dependencia severa/profunda o NEE": 0.64,
    },
    "18-59": {
        "Sin discapacidad, dependencia o NEE": 0.00,
        "Discapacidad Leve": 0.34,
        "Discapacidad o dependencia moderada": 0.52,
        "Discapacidad o dependencia severa/profunda o NEE": 0.64,
    },
    "60-74": {
        "Sin discapacidad, dependencia o NEE": 0.61,
        "Discapacidad Leve": 0.68,
        "Discapacidad o dependencia moderada": 0.82,
        "Discapacidad o dependencia severa/profunda o NEE": 1.01,
    },
    "75+": {
        "Sin discapacidad, dependencia o NEE": 0.75,
        "Discapacidad Leve": 0.77,
        "Discapacidad o dependencia moderada": 0.82,
        "Discapacidad o dependencia severa/profunda o NEE": 1.01,
    },
}


def obtener_rango_edad(edad):
    """Retorna la clave del rango de edad para la tabla de coeficientes."""
    if edad <= 5:
        return "0-5"
    elif edad <= 14:
        return "6-14"
    elif edad <= 17:
        return "15-17"
    elif edad <= 59:
        return "18-59"
    elif edad <= 74:
        return "60-74"
    else:
        return "75+"


def obtener_opciones_discapacidad(rango_edad):
    """Retorna las opciones de discapacidad disponibles para un rango de edad."""
    return list(COEFICIENTES[rango_edad].keys())


def obtener_coeficiente(edad, condicion):
    """Obtiene el coeficiente Y para una edad y condición dadas."""
    rango = obtener_rango_edad(edad)
    return COEFICIENTES[rango].get(condicion, 0.0)