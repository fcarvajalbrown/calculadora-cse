"""
Aplicación principal de la calculadora CSE
"""

import tkinter as tk
from tkinter import ttk, messagebox

from calculator.income import calcular_ingreso_equivalente, determinar_tramo_por_ingreso
from calculator.needs_index import calcular_indice_necesidades, calcular_ingreso_corregido
from calculator.means_test import evaluar_test_medios
from gui.integrante_frame import IntegranteFrame
from gui.medios_frame import TestMediosFrame
from gui.report import generar_reporte


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
        self._build_header()
        
        # --- Notebook (pestañas) ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Pestaña 1: Integrantes
        self._build_tab_integrantes()
        
        # Pestaña 2: Test de Medios
        self._build_tab_medios()
        
        # Pestaña 3: Resultados
        self._build_tab_resultados()

        # --- Botón Calcular ---
        self._build_footer()

    def _build_header(self):
        """Construye el header de la aplicación."""
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10, pady=5)
        ttk.Label(header, text="Calculadora de Calificación Socioeconómica (CSE)",
                  font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(header, text="Registro Social de Hogares - Resolución Exenta N°082",
                  font=("Segoe UI", 9), foreground="gray").pack()

    def _build_tab_integrantes(self):
        """Construye la pestaña de integrantes."""
        self.tab_integrantes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_integrantes, text="  Integrantes del Hogar  ")

        btn_frame = ttk.Frame(self.tab_integrantes)
        btn_frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(btn_frame, text="+ Agregar Integrante", command=self._agregar_integrante).pack(side="left")
        ttk.Label(btn_frame, 
                 text="  Ingrese los datos de cada integrante del hogar (ingresos promedio mensual últimos 12 meses)",
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

    def _build_tab_medios(self):
        """Construye la pestaña de test de medios."""
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

    def _build_tab_resultados(self):
        """Construye la pestaña de resultados."""
        self.tab_resultados = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_resultados, text="  Resultados  ")

        self.resultado_text = tk.Text(self.tab_resultados, wrap="word", font=("Consolas", 10),
                                      state="disabled", bg="#fafafa")
        self.resultado_text.pack(fill="both", expand=True, padx=10, pady=10)

    def _build_footer(self):
        """Construye el footer con botón de cálculo."""
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=10, pady=8)
        btn_calc = ttk.Button(bottom, text="CALCULAR CALIFICACIÓN SOCIOECONÓMICA",
                              command=self._calcular)
        btn_calc.pack(fill="x", ipady=8)

    def _agregar_integrante(self):
        """Agrega un nuevo frame de integrante."""
        self.contador_integrantes += 1
        frame = IntegranteFrame(self.scroll_frame, self.contador_integrantes,
                                on_delete=self._eliminar_integrante)
        frame.pack(fill="x", padx=5, pady=4)
        self.integrantes_frames.append(frame)

    def _eliminar_integrante(self, frame):
        """Elimina un frame de integrante."""
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
        """Ejecuta el cálculo completo de la CSE."""
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

        # --- Generar reporte ---
        resultado = generar_reporte(
            integrantes, ingreso_equiv, indice_nec, ingreso_corregido,
            tramo_ingreso, tramo_medios, num_medios, detalle_medios
        )

        # Mostrar resultados
        self.resultado_text.configure(state="normal")
        self.resultado_text.delete("1.0", "end")
        self.resultado_text.insert("1.0", resultado)
        self.resultado_text.configure(state="disabled")

        # Ir a pestaña de resultados
        self.notebook.select(self.tab_resultados)