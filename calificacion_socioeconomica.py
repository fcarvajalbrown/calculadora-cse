"""
Calculadora de Calificación Socioeconómica (CSE)
Basado en: Orientaciones para el Cálculo de la Calificación Socioeconómica
Resolución Exenta N°082, Junio 2024
Departamento de Operaciones - División de Focalización

DISCLAIMER:
    Esta herramienta es de carácter EDUCATIVO y REFERENCIAL.
    NO reemplaza el cálculo oficial realizado por el Ministerio de
    Desarrollo Social y Familia (MDSF) a través del Registro Social de Hogares.
    Los umbrales de tramos utilizados son aproximaciones referenciales,
    ya que los valores oficiales basados en la encuesta CASEN no son públicos.
    Para información oficial visite: https://www.registrosocial.gob.cl
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math


# ============================================================
# TABLA DE COEFICIENTES (Tabla N°1 - Resolución Exenta N°082)
# ============================================================
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

FACTOR_ESCALA = 0.7


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


def calcular_ingreso_equivalente(integrantes):
    """Calcula el ingreso equivalente del hogar (suma de ingresos de mayores de 18)."""
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
            salario_minimo = 500000  # Valor referencial del salario mínimo
            ingreso_total_persona = ing_trabajo + ing_pension + ing_capital
            umbral = 2 * salario_minimo
            if ingreso_total_persona > umbral:
                total += ingreso_total_persona - umbral
        else:
            total += ing_trabajo + ing_pension + ing_capital

    return total


def calcular_indice_necesidades(integrantes):
    """
    Calcula el Índice de Necesidades (IN).
    IN = N^0.7 + Y1 + Y2 + ... + Yn
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
    """Ingreso equivalente corregido = Ingreso equivalente / Índice de necesidades."""
    if indice_necesidades == 0:
        return 0
    return ingreso_equivalente / indice_necesidades


def evaluar_test_medios(datos_medios):
    """
    Evalúa los test de medios y retorna el tramo inferido más alto.
    Retorna: (tramo_inferido, medios_activos, detalle)
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

    # Si hay mezcla, tomar el máximo
    if total_medios_muy_alto >= 1 and total_medios_alto >= 1:
        # Ya se tiene al menos tramo 90 por muy alto valor
        pass

    total_medios = total_medios_alto + total_medios_muy_alto
    return tramo_inferido, total_medios, detalle


def determinar_tramo_por_ingreso(ingreso_corregido):
    """
    Determina el tramo de la CSE según el ingreso equivalente corregido.
    Utiliza umbrales referenciales basados en CASEN.
    """
    # Umbrales referenciales (valores aproximados)
    if ingreso_corregido <= 82174:
        return 40
    elif ingreso_corregido <= 136382:
        return 50
    elif ingreso_corregido <= 214052:
        return 60
    elif ingreso_corregido <= 340205:
        return 70
    elif ingreso_corregido <= 559341:
        return 80
    elif ingreso_corregido <= 1043790:
        return 90
    else:
        return 100


# ============================================================
# INTERFAZ GRÁFICA
# ============================================================

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


class AplicacionCSE(tk.Tk):
    """Aplicación principal para el cálculo de la Calificación Socioeconómica."""

    def __init__(self):
        super().__init__()
        self.title("Calculadora de Calificación Socioeconómica (CSE)")
        self.geometry("820x850")
        self.minsize(820, 700)
        self.configure(bg="#f0f0f0")

        self.integrantes_frames = []
        self.contador_integrantes = 0

        self._build_ui()
        self._agregar_integrante()  # Agregar al menos 1 integrante

    def _build_ui(self):
        # --- Título ---
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10, pady=5)
        ttk.Label(header, text="Calculadora de Calificación Socioeconómica (CSE)",
                  font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(header, text="Registro Social de Hogares - Resolución Exenta N°082",
                  font=("Segoe UI", 9), foreground="gray").pack()

        # --- Notebook (pestañas) ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Pestaña 1: Integrantes
        self.tab_integrantes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_integrantes, text="  Integrantes del Hogar  ")

        btn_frame = ttk.Frame(self.tab_integrantes)
        btn_frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(btn_frame, text="+ Agregar Integrante", command=self._agregar_integrante).pack(side="left")
        ttk.Label(btn_frame, text="  Ingrese los datos de cada integrante del hogar (ingresos promedio mensual últimos 12 meses)",
                  foreground="gray").pack(side="left", padx=10)

        # Canvas con scroll para integrantes
        container = ttk.Frame(self.tab_integrantes)
        container.pack(fill="both", expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = ttk.Frame(self.canvas)

        self.scroll_frame.bind("<Configure>",
                               lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Scroll con rueda del mouse
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Pestaña 2: Test de Medios
        self.tab_medios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_medios, text="  Test de Medios  ")

        medios_container = ttk.Frame(self.tab_medios)
        medios_container.pack(fill="both", expand=True, padx=5, pady=5)

        medios_canvas = tk.Canvas(medios_container, highlightthickness=0)
        medios_scroll = ttk.Scrollbar(medios_container, orient="vertical", command=medios_canvas.yview)
        medios_inner = ttk.Frame(medios_canvas)

        medios_inner.bind("<Configure>",
                          lambda e: medios_canvas.configure(scrollregion=medios_canvas.bbox("all")))
        medios_canvas.create_window((0, 0), window=medios_inner, anchor="nw")
        medios_canvas.configure(yscrollcommand=medios_scroll.set)

        medios_canvas.pack(side="left", fill="both", expand=True)
        medios_scroll.pack(side="right", fill="y")

        self.test_medios = TestMediosFrame(medios_inner)
        self.test_medios.pack(fill="x", padx=5, pady=5)

        # Pestaña 3: Resultados
        self.tab_resultados = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_resultados, text="  Resultados  ")

        self.resultado_text = tk.Text(self.tab_resultados, wrap="word", font=("Consolas", 10),
                                      state="disabled", bg="#fafafa")
        self.resultado_text.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Botón Calcular ---
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=10, pady=8)
        btn_calc = ttk.Button(bottom, text="CALCULAR CALIFICACIÓN SOCIOECONÓMICA",
                              command=self._calcular)
        btn_calc.pack(fill="x", ipady=8)

    def _agregar_integrante(self):
        self.contador_integrantes += 1
        frame = IntegranteFrame(self.scroll_frame, self.contador_integrantes,
                                on_delete=self._eliminar_integrante)
        frame.pack(fill="x", padx=5, pady=4)
        self.integrantes_frames.append(frame)

    def _eliminar_integrante(self, frame):
        if len(self.integrantes_frames) <= 1:
            messagebox.showwarning("Aviso", "El hogar debe tener al menos 1 integrante.")
            return
        frame.destroy()
        self.integrantes_frames.remove(frame)
        # Renumerar
        for i, f in enumerate(self.integrantes_frames, 1):
            f.configure(text=f"  Integrante {i}  ")
            f.numero = i

    def _calcular(self):
        try:
            integrantes = [f.obtener_datos() for f in self.integrantes_frames]
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer datos de integrantes:\n{e}")
            return

        if not integrantes:
            messagebox.showwarning("Aviso", "Debe ingresar al menos un integrante.")
            return

        # --- Paso 1: Ingreso equivalente ---
        ingreso_equiv = calcular_ingreso_equivalente(integrantes)

        # --- Paso 2: Índice de necesidades ---
        indice_nec = calcular_indice_necesidades(integrantes)

        # --- Paso 3: Ingreso equivalente corregido ---
        ingreso_corregido = calcular_ingreso_corregido(ingreso_equiv, indice_nec)

        # --- Paso 4: Tramo por ingresos ---
        tramo_ingreso = determinar_tramo_por_ingreso(ingreso_corregido)

        # --- Paso 5: Test de medios ---
        datos_medios = self.test_medios.obtener_datos()
        tramo_medios, num_medios, detalle_medios = evaluar_test_medios(datos_medios)

        # --- Tramo final: el mayor entre ingreso y medios ---
        tramo_final = max(tramo_ingreso, tramo_medios)

        # --- Construir reporte ---
        lineas = []
        lineas.append("=" * 70)
        lineas.append("   RESULTADO - CALIFICACIÓN SOCIOECONÓMICA (CSE)")
        lineas.append("=" * 70)
        lineas.append("")

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
                salario_minimo = 500000
                umbral = 2 * salario_minimo
                if total_persona > umbral:
                    nota = f" (estudia 18-24: se considera ${total_persona - umbral:,.0f})"
                else:
                    nota = f" (estudia 18-24: no supera 2 salarios mínimos, no se considera)"
            lineas.append(f"  {nombre} ({edad} años):")
            lineas.append(f"    Trabajo: ${it:>12,.0f}  |  Pensión: ${ip:>12,.0f}  |  Capital: ${ic:>12,.0f}{nota}")

        lineas.append(f"\n  >> Ingreso equivalente del hogar = ${ingreso_equiv:,.0f}")
        lineas.append("")

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

        lineas.append("PASO 3: INGRESO EQUIVALENTE CORREGIDO")
        lineas.append("-" * 50)
        lineas.append(f"  Ingreso equivalente / Índice de necesidades")
        lineas.append(f"  = ${ingreso_equiv:,.0f} / {indice_nec:.8f}")
        lineas.append(f"\n  >> Ingreso equivalente corregido = ${ingreso_corregido:,.0f}")
        lineas.append("")

        lineas.append("PASO 4: TRAMO POR INGRESOS")
        lineas.append("-" * 50)
        lineas.append(f"  >> Tramo inicial por ingresos = {tramo_ingreso}% de la CSE")
        lineas.append("")

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

        tramo_desc = {
            40: "Tramo 40% - Hogares de menores ingresos",
            50: "Tramo 50%",
            60: "Tramo 60%",
            70: "Tramo 70%",
            80: "Tramo 80%",
            90: "Tramo 90%",
            100: "Tramo 100% - Hogares de mayores ingresos",
        }
        lineas.append(f"  {tramo_desc.get(tramo_final, '')}")

        # Mostrar resultados
        resultado = "\n".join(lineas)
        self.resultado_text.configure(state="normal")
        self.resultado_text.delete("1.0", "end")
        self.resultado_text.insert("1.0", resultado)
        self.resultado_text.configure(state="disabled")

        # Ir a pestaña de resultados
        self.notebook.select(self.tab_resultados)


def main():
    app = AplicacionCSE()
    app.mainloop()


if __name__ == "__main__":
    main()
