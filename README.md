# Predicción de procesos de compra sin adjudicación

Proyecto final de Aprendizaje Automático desarrollado por Florencia Farías.

## Objetivo

El objetivo del proyecto es construir un modelo de clasificación que permita anticipar, desde el momento de publicación de una compra, si el proceso podría finalizar sin adjudicación.

La predicción funciona como una alerta temprana y no como una decisión automática.

## Origen de los datos

Los datos provienen del sistema público Buenos Aires Compras y fueron descargados el 29 de octubre de 2026.

Los registros analizados corresponden al período comprendido entre el 3 de enero y el 3 de junio de 2022.

## Archivos utilizados

| Archivo | Filas | Columnas | Contenido |
|---|---:|---:|---|
| `main.csv` | 23.298 | 33 | Información general de los procesos |
| `tender_items.csv` | 23.298 | 11 | Renglones solicitados |
| `awards.csv` | 13.835 | 12 | Adjudicaciones |
| `awards_items.csv` | 13.835 | 12 | Renglones adjudicados |

## Relaciones entre los archivos

- `main.csv` se relaciona con `tender_items.csv` mediante `_link` y `_link_main`.
- `main.csv` se relaciona con `awards.csv` mediante `_link` y `_link_main`.
- `awards.csv` se relaciona con `awards_items.csv` mediante `_link` y `_link_main`.
- `tender_id` identifica cada proceso de compra.

## Preparación de los datos

Se realizaron los siguientes controles y transformaciones:

- Revisión de dimensiones y tipos de datos.
- Análisis de valores faltantes.
- Control de filas duplicadas.
- Validación de los estados repetidos por proceso.
- Consolidación de una observación por `tender_id`.
- Comprobación de la vinculación de las adjudicaciones.
- Conversión de fechas.
- Tratamiento de organismos compradores faltantes.
- Codificación One-Hot de variables categóricas.
- Separación de entrenamiento y evaluación.
- Exclusión de variables que revelarían el resultado final.

Se comprobó que las 13.835 adjudicaciones se vinculan con el archivo principal y que no existen adjudicaciones sin relacionar.

## Variable objetivo

La variable objetivo es `sin_adjudicacion`:

- `0`: proceso con adjudicación.
- `1`: proceso finalizado sin adjudicación.

Los procesos activos y los procesos sin estado fueron excluidos.

El dataset final contiene 2.276 procesos:

- 1.757 con adjudicación.
- 519 sin adjudicación.

La categoría sin adjudicación incluye procesos cancelados, no exitosos y procesos completos sin una adjudicación asociada. Por lo tanto, no todos representan la misma causa.

## Momento de la predicción

La predicción se plantea para el momento de publicación de la compra.

Por este motivo, el estado final, la existencia de adjudicaciones y los archivos `awards.csv` y `awards_items.csv` fueron utilizados para construir la etiqueta, pero no como predictores del modelo.

## Variables predictoras

- Modalidad de contratación.
- Indicador de procedimiento competitivo.
- Duración del período de recepción de ofertas.
- Duración del período de consultas.
- Organismo comprador.
- Indicador de acuerdo marco.
- Cantidad de renglones del proceso.

## Modelos evaluados

Se compararon dos modelos de clasificación:

1. Regresión logística.
2. Árbol de decisión con profundidad máxima de 5.

## Resultados

| Modelo | Accuracy | Precisión | Recall | F1-score |
|---|---:|---:|---:|---:|
| Regresión logística | 0,759 | 0,250 | 0,029 | 0,052 |
| Árbol de decisión | 0,897 | 0,967 | 0,567 | 0,715 |

El árbol de decisión presentó el mejor desempeño.

De los 104 procesos sin adjudicación del conjunto de evaluación, identificó correctamente 59. Solamente generó 2 falsas alertas.

La característica más importante fue la cantidad de renglones del proceso.

## Limitaciones

El modelo todavía no detecta todos los procesos sin adjudicación. Además, los datos corresponden a un período limitado de 2022, por lo que los resultados no deben interpretarse como una garantía para períodos futuros.

## Estructura principal

```text
data/
├── raw/              Datos originales
└── processed/        Dataset preparado para el modelo

notebooks/
└── 01_exploracion_dataset_compras.ipynb

requirements.txt
README.md
```

## Ejecución

Clonar el repositorio e instalar las dependencias:

```bash
pip install -r requirements.txt
```

Luego ejecutar:

```bash
jupyter notebook notebooks/01_exploracion_dataset_compras.ipynb
```

El dataset procesado se encuentra en:

```text
data/processed/dataset_modelo.csv
```

## Conclusión

El árbol de decisión puede utilizarse como herramienta de apoyo para identificar procesos con riesgo de finalizar sin adjudicación. Su precisión es elevada, aunque debe complementarse con revisión humana y con nuevas extracciones de datos para mejorar su capacidad de detección.