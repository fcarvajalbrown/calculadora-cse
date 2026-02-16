"""
Frame para test de medios (factores de reordenamiento)
"""

import tkinter as tk
from tkinter import ttk


class TestMediosFrame(ttk.LabelFrame):
    """Frame para los test de medios (factores de reordenamiento)."""

    def __init__(self, parent):
        super().__init__(parent, text="  Test de Medios (Factores de Reordenamiento)  ", padding=10)
        self._build()

    def _build(self):
        info = ttk.Label(self, text=(
            "Marque los test de medios que aplican al hogar. Estos permiten verificar la consistencia\n"
            "entre los ingresos del hogar y su estándar de vida."
        ), foreground="gray", wraplength=700, justify="left")
        info.pack(fill="x", pady=(0, 8))

        # --- 1. Cotización de salud ---
        lf1 = ttk.LabelFrame(self, text="  1. Valor de la cotización de salud  ", padding=5)
        lf1.pack(fill="x", pady=3)
        self.salud_alto = tk.BooleanVar()
        self.salud_muy_alto = tk.BooleanVar()
        ttk.Checkbutton(lf1, text="Plan de ALTO valor (sobre el 30% de los planes más costosos) -> Tramo 50",
                        variable=self.salud_alto).pack(anchor="w")
        ttk.Checkbutton(lf1, text="Plan de MUY ALTO valor (sobre el 65% de los planes más costosos) -> Tramo 90",
                        variable=self.salud_muy_alto).pack(anchor="w")

        # --- 2. Matrícula educacional ---
        lf2 = ttk.LabelFrame(self, text="  2. Matrícula en establecimiento educacional de alto valor  ", padding=5)
        lf2.pack(fill="x", pady=3)
        self.educacion_alto = tk.BooleanVar()
        ttk.Checkbutton(lf2,
                        text="Mensualidad >= $100.000 (prebásica, básica o media) [Se activa solo con otro medio]",
                        variable=self.educacion_alto).pack(anchor="w")

        # --- 3. Vehículos y embarcaciones ---
        lf3 = ttk.LabelFrame(self, text="  3. Vehículos terrestres y/o embarcaciones marítimas  ", padding=5)
        lf3.pack(fill="x", pady=3)
        self.vehiculos_alto = tk.BooleanVar()
        self.vehiculos_muy_alto = tk.BooleanVar()
        self.nave_mayor = tk.BooleanVar()
        self.tres_naves = tk.BooleanVar()
        ttk.Checkbutton(lf3, text="ALTO valor: Avalúo >= 20% de la tasación fiscal más costosa -> Tramo 50",
                        variable=self.vehiculos_alto).pack(anchor="w")
        ttk.Checkbutton(lf3, text="MUY ALTO valor: Avalúo >= 5% de la tasación fiscal más costosa -> Tramo 90",
                        variable=self.vehiculos_muy_alto).pack(anchor="w")
        ttk.Checkbutton(lf3, text="Al menos una nave mayor (DIRECTEMAR) -> Tramo 90",
                        variable=self.nave_mayor).pack(anchor="w")
        ttk.Checkbutton(lf3, text="3 o más naves menores y/o deportivas -> Tramo 90",
                        variable=self.tres_naves).pack(anchor="w")

        # --- 4. Bienes raíces ---
        lf4 = ttk.LabelFrame(self, text="  4. Bienes raíces  ", padding=5)
        lf4.pack(fill="x", pady=3)
        self.bienes_alto = tk.BooleanVar()
        self.bienes_muy_alto = tk.BooleanVar()
        ttk.Checkbutton(lf4,
                        text="ALTO valor: Avalúo >= 20% de la tasación fiscal más costosa [Se activa con otro medio]",
                        variable=self.bienes_alto).pack(anchor="w")
        ttk.Checkbutton(lf4, text="MUY ALTO valor: Avalúo >= 5% de la tasación fiscal más costosa -> Tramo 90",
                        variable=self.bienes_muy_alto).pack(anchor="w")

        # --- 5. Ingresos padre/madre no presente ---
        lf5 = ttk.LabelFrame(self, text="  5. Ingresos del padre o madre no presente en el hogar  ", padding=5)
        lf5.pack(fill="x", pady=3)
        ttk.Label(lf5, text=(
            "Se activa cuando el padre/madre fuera del hogar tiene altos ingresos\n"
            "y hay hijos < 21 años (o 21-24 estudiando) en el hogar."
        ), foreground="gray", wraplength=650, justify="left").pack(anchor="w", pady=(0, 4))
        self.padre_alto = tk.BooleanVar()
        self.padre_muy_alto = tk.BooleanVar()
        ttk.Checkbutton(lf5,
                        text="ALTO valor: Ingreso entre percentil 78-90 de mayores ingresos -> Tramo 80",
                        variable=self.padre_alto).pack(anchor="w")
        ttk.Checkbutton(lf5,
                        text="MUY ALTO valor: Ingreso en percentil 91 o superior -> Tramo 90",
                        variable=self.padre_muy_alto).pack(anchor="w")

    def obtener_datos(self):
        """Retorna diccionario con todos los flags de test de medios."""
        return {
            "salud_alto_valor": self.salud_alto.get(),
            "salud_muy_alto_valor": self.salud_muy_alto.get(),
            "educacion_alto_valor": self.educacion_alto.get(),
            "vehiculos_alto_valor": self.vehiculos_alto.get(),
            "vehiculos_muy_alto_valor": self.vehiculos_muy_alto.get(),
            "nave_mayor": self.nave_mayor.get(),
            "tres_naves_menores": self.tres_naves.get(),
            "bienes_raices_alto_valor": self.bienes_alto.get(),
            "bienes_raices_muy_alto_valor": self.bienes_muy_alto.get(),
            "padre_madre_alto_valor": self.padre_alto.get(),
            "padre_madre_muy_alto_valor": self.padre_muy_alto.get(),
        }