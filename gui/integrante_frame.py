"""
Frame para datos de un integrante del hogar
"""

import tkinter as tk
from tkinter import ttk
from calculator.coefficients import obtener_rango_edad, obtener_opciones_discapacidad


class IntegranteFrame(ttk.LabelFrame):
    """Frame para ingresar los datos de un integrante del hogar."""

    def __init__(self, parent, numero, on_delete=None):
        super().__init__(parent, text=f"  Integrante {numero}  ", padding=10)
        self.numero = numero
        self.on_delete = on_delete
        self._build()

    def _build(self):
        # --- Fila 1: Nombre y Edad ---
        f1 = ttk.Frame(self)
        f1.pack(fill="x", pady=2)

        ttk.Label(f1, text="Nombre:", width=12).pack(side="left")
        self.nombre_var = tk.StringVar(value=f"Integrante {self.numero}")
        ttk.Entry(f1, textvariable=self.nombre_var, width=20).pack(side="left", padx=(0, 15))

        ttk.Label(f1, text="Edad:", width=6).pack(side="left")
        self.edad_var = tk.IntVar(value=30)
        edad_spin = ttk.Spinbox(f1, from_=0, to=120, textvariable=self.edad_var, width=5,
                                command=self._actualizar_condiciones)
        edad_spin.pack(side="left", padx=(0, 15))

        # Checkbox: estudia (solo relevante para 18-24)
        self.estudia_var = tk.BooleanVar(value=False)
        self.chk_estudia = ttk.Checkbutton(f1, text="Estudia (18-24 años)", variable=self.estudia_var)
        self.chk_estudia.pack(side="left", padx=(0, 10))

        # Botón eliminar
        if self.on_delete:
            ttk.Button(f1, text="X", width=3, command=lambda: self.on_delete(self)).pack(side="right")

        # --- Fila 2: Condición de discapacidad ---
        f2 = ttk.Frame(self)
        f2.pack(fill="x", pady=2)

        ttk.Label(f2, text="Condición:", width=12).pack(side="left")
        self.condicion_var = tk.StringVar()
        self.combo_condicion = ttk.Combobox(f2, textvariable=self.condicion_var, state="readonly", width=55)
        self.combo_condicion.pack(side="left", padx=(0, 10))

        # --- Fila 3: Ingresos ---
        f3 = ttk.Frame(self)
        f3.pack(fill="x", pady=2)

        ttk.Label(f3, text="Ing. Trabajo:", width=12).pack(side="left")
        self.ing_trabajo_var = tk.StringVar(value="0")
        ttk.Entry(f3, textvariable=self.ing_trabajo_var, width=15).pack(side="left", padx=(0, 10))

        ttk.Label(f3, text="Ing. Pensión:", width=12).pack(side="left")
        self.ing_pension_var = tk.StringVar(value="0")
        ttk.Entry(f3, textvariable=self.ing_pension_var, width=15).pack(side="left", padx=(0, 10))

        ttk.Label(f3, text="Ing. Capital:", width=12).pack(side="left")
        self.ing_capital_var = tk.StringVar(value="0")
        ttk.Entry(f3, textvariable=self.ing_capital_var, width=15).pack(side="left")

        self._actualizar_condiciones()

    def _actualizar_condiciones(self):
        """Actualiza las opciones del combobox según la edad."""
        try:
            edad = self.edad_var.get()
        except tk.TclError:
            edad = 30
        rango = obtener_rango_edad(edad)
        opciones = obtener_opciones_discapacidad(rango)
        self.combo_condicion["values"] = opciones
        if self.condicion_var.get() not in opciones:
            self.condicion_var.set(opciones[0])

    def obtener_datos(self):
        """Retorna un diccionario con los datos del integrante."""
        def parse_monto(val):
            txt = val.strip().replace("$", "").replace(".", "").replace(",", "")
            return max(0, int(txt)) if txt else 0

        return {
            "nombre": self.nombre_var.get(),
            "edad": self.edad_var.get(),
            "condicion": self.condicion_var.get(),
            "estudia": self.estudia_var.get(),
            "ingreso_trabajo": parse_monto(self.ing_trabajo_var.get()),
            "ingreso_pension": parse_monto(self.ing_pension_var.get()),
            "ingreso_capital": parse_monto(self.ing_capital_var.get()),
        }