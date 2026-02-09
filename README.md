# Calculadora de Calificacion Socioeconomica (CSE)

Herramienta en Python con interfaz grafica (Tkinter) que permite calcular la **Calificacion Socioeconomica** de un hogar, siguiendo la metodologia descrita en el documento oficial *"Orientaciones para el Calculo de la Calificacion Socioeconomica"* (Resolucion Exenta N 082, Junio 2024) del Ministerio de Desarrollo Social y Familia de Chile.

## Que es la Calificacion Socioeconomica?

La CSE es una medida que ordena a los hogares del Registro Social de Hogares (RSH) en **7 tramos** (40% al 100%), de acuerdo a variables relacionadas con los ingresos economicos y el estandar de vida del hogar. Es utilizada para focalizar prestaciones sociales del Estado chileno.

## Que calcula esta herramienta?

La aplicacion implementa paso a paso la metodologia oficial:

### Paso 1 - Ingreso equivalente del hogar
Suma de los ingresos del trabajo, pensiones y capital de todos los integrantes mayores de 18 anios (promedio mensual de los ultimos 12 meses).

### Paso 2 - Indice de Necesidades (IN)
Considera la composicion del hogar aplicando la formula:

```
IN = N^0.7 + Y1 + Y2 + ... + Yn
```

Donde:
- **N** = numero de integrantes del hogar
- **0.7** = factor exponencial de economias de escala
- **Y** = coeficiente individual segun edad y condicion de discapacidad/dependencia

### Paso 3 - Ingreso equivalente corregido

```
Ingreso corregido = Ingreso equivalente / Indice de necesidades
```

### Paso 4 - Tramo inicial por ingresos
Ubica al hogar en un tramo segun umbrales referenciales.

### Paso 5 - Test de Medios (Factores de reordenamiento)
Evalua la consistencia entre ingresos y estandar de vida del hogar:

1. **Cotizacion de salud** - Planes de alto/muy alto valor
2. **Matricula educacional** - Establecimientos con mensualidad >= $100.000
3. **Vehiculos terrestres y embarcaciones** - Avaluo fiscal alto/muy alto valor
4. **Bienes raices** - Avaluo fiscal alto/muy alto valor
5. **Ingresos padre/madre no presente** - Altos ingresos de progenitor fuera del hogar

## Tabla de coeficientes individuales

| Edad | Sin discapacidad/dependencia | Leve | Moderada | Severa/Profunda o NEE |
|------|------------------------------|------|----------|-----------------------|
| 0-5 | 0.40 | - | - | 0.80 |
| 6-14 | 0.30 | 0.34 | 0.52 | 0.64 |
| 15-17 | 0.09 | 0.34 | 0.52 | 0.64 |
| 18-59 | 0.00 | 0.34 | 0.52 | 0.64 |
| 60-74 | 0.61 | 0.68 | 0.82 | 1.01 |
| 75+ | 0.75 | 0.77 | 0.82 | 1.01 |

*Fuente: Tabla N 1 - Resolucion Exenta N 082*

## Requisitos

- Python 3.6 o superior
- Tkinter (incluido por defecto en la mayoria de instalaciones de Python)

## Uso

```bash
python calificacion_socioeconomica.py
```

La aplicacion tiene 3 pestanias:

1. **Integrantes del Hogar** - Agregar/eliminar integrantes con sus datos personales e ingresos
2. **Test de Medios** - Marcar los factores de reordenamiento que aplican
3. **Resultados** - Ver el calculo detallado paso a paso y el tramo final

## Ejemplo

Hogar de 3 integrantes (ejemplo del documento oficial):

| Integrante | Edad | Ing. Trabajo | Ing. Pension | Ing. Capital |
|------------|------|-------------|-------------|-------------|
| Maria | 35 | $500.000 | $0 | $100.000 |
| Alejandro | 38 | $300.000 | $200.000 | $0 |
| Pablo | 8 | $0 | $0 | $0 |

**Resultados:**
- Ingreso equivalente: $1.100.000
- Indice de necesidades: 2,4577
- Ingreso equivalente corregido: $447.578

## Disclaimer

> **Esta herramienta es de caracter EDUCATIVO y REFERENCIAL.**
> No reemplaza el calculo oficial realizado por el Ministerio de Desarrollo Social y Familia (MDSF) a traves del Registro Social de Hogares. Los umbrales de tramos utilizados son aproximaciones referenciales, ya que los valores oficiales basados en la encuesta CASEN no son publicos.
>
> Para informacion oficial visite: https://www.registrosocial.gob.cl

## Referencia

- [Orientaciones para el Calculo de la Calificacion Socioeconomica](https://www.registrosocial.gob.cl) - Resolucion Exenta N 082, Junio 2024, Departamento de Operaciones, Division de Focalizacion.

## Licencia

Este proyecto esta bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para mas detalles.
