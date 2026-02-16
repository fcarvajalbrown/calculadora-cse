"""
Calculadora de Calificación Socioeconómica (CSE)
Basado en: Resolución Exenta N°082, Junio 2024

DISCLAIMER:
    Esta herramienta es de carácter EDUCATIVO y REFERENCIAL.
    NO reemplaza el cálculo oficial realizado por el Ministerio de
    Desarrollo Social y Familia (MDSF) a través del Registro Social de Hogares.
"""

from gui.app import AplicacionCSE


def main():
    app = AplicacionCSE()
    app.mainloop()


if __name__ == "__main__":
    main()