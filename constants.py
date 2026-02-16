"""
Constantes globales de la aplicación CSE
"""

# Salario mínimo referencial (CLP)
SALARIO_MINIMO = 500000

# Factor de escala para el cálculo del índice de necesidades
FACTOR_ESCALA = 0.7

# Umbrales de tramos por ingreso (valores referenciales basados en CASEN)
UMBRALES_INGRESO = [
    (82174, 40),
    (136382, 50),
    (214052, 60),
    (340205, 70),
    (559341, 80),
    (1043790, 90),
    (float('inf'), 100)
]

# Descripciones de tramos
TRAMO_DESCRIPCIONES = {
    40: "Tramo 40% - Hogares de menores ingresos",
    50: "Tramo 50%",
    60: "Tramo 60%",
    70: "Tramo 70%",
    80: "Tramo 80%",
    90: "Tramo 90%",
    100: "Tramo 100% - Hogares de mayores ingresos",
}