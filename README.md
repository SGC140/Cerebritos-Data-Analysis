# Procesamiento y Agregación de Logs de Gamificación

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![License](https://img.shields.io/badge/License-Proprietary-blue)

Este repositorio contiene un script de Python diseñado para consolidar, limpiar y agregar datos de logs de gamificación provenientes de múltiples fuentes CSV. El objetivo principal es transformar datos brutos y fragmentados en un formato estructurado y analizable, facilitando la medición del engagement de los usuarios y el rendimiento por nivel educativo.

## Índice

1.  [Visión General del Proyecto](#1-visión-general-del-proyecto)
2.  [Arquitectura y Lógica del Pipeline](#2-arquitectura-y-lógica-del-pipeline)
    *   [Payload de Entrada](#payload-de-entrada)
    *   [Flujo del Pipeline](#flujo-del-pipeline)
3.  [Configuración y Dependencias](#3-configuración-y-dependencias)
    *   [Dependencias del Sistema Operativo](#dependencias-del-sistema-operativo)
    *   [Dependencias de Python](#dependencias-de-python)
    *   [Instalación](#instalación)
4.  [Estructura de Salida de Datos](#4-estructura-de-salida-de-datos)
    *   [Cerebros_parcial.csv](#cerebros_parcialcsv)
    *   [CSV_AGRUPADO.csv](#csv_agrupadocsv)
5.  [Análisis Técnico y Justificación de Librerías](#5-análisis-técnico-y-justificación-de-librerías)
6.  [Valor de Negocio y Aplicaciones](#6-valor-de-negocio-y-aplicaciones)
    *   [Preguntas de Negocio Abordadas](#preguntas-de-negocio-abordadas)
    *   [Valor Agregado](#valor-agregado)
    *   [Capacidades de Medición y Diagnóstico](#capacidades-de-medición-y-diagnóstico)
    *   [Resolución, Optimización y Estandarización](#resolución-optimización-y-estandarización)
    *   [Oportunidades de Repensar Estrategias](#oportunidades-de-repensar-estrategias)

---

## 1. Visión General del Proyecto

Este proyecto aborda la necesidad de consolidar y estandarizar datos de gamificación dispersos en múltiples archivos CSV. El script `main.py` automatiza la fusión de estos datasets, la selección y renombramiento de columnas clave, la normalización de identificadores de nivel educativo y la agregación de métricas de engagement. El resultado es un conjunto de datos limpio y listo para análisis, que permite una comprensión profunda del comportamiento del usuario dentro del sistema de gamificación.

## 2. Arquitectura y Lógica del Pipeline

La arquitectura del proyecto es de tipo ETL (Extract, Transform, Load) basada en un script monolítico de Python.

### Payload de Entrada

El pipeline requiere dos archivos CSV de entrada ubicados en el mismo directorio que el script `main.py`:

*   `Gamificación ago- dic.csv`: Contiene logs de gamificación de un período inicial.
*   `kuepa_sis.gamification_logsDic02-Mar1.csv`: Contiene logs de gamificación de un período posterior.

Ambos archivos deben contener columnas que permitan la extracción de `_id`, `user`, `increm[0]`, `correo[0]`, `Nivel[0][0]`, `logs[0].stats[0].value`, `logs[0].stats[0].message`, y `created_at`.

### Flujo del Pipeline

El script `main.py` ejecuta la siguiente secuencia de operaciones:

1.  **Extracción y Consolidación (Extract & Concatenate):**
    *   Carga `Gamificación ago- dic.csv` y `kuepa_sis.gamification_logsDic02-Mar1.csv` en DataFrames de Pandas.
    *   Concatena ambos DataFrames verticalmente para crear un dataset unificado.
    *   Guarda el dataset consolidado inicial como `cerebritos.csv`.

    ```python
    import pandas as pd

    data1 = pd.read_csv("Gamificación ago- dic.csv")
    data2 = pd.read_csv("kuepa_sis.gamification_logsDic02-Mar1.csv")
    data = pd.concat([data1, data2])
    data.to_csv("cerebritos.csv")
    ```

2.  **Selección y Renombramiento de Columnas (Transform - Selection & Renaming):**
    *   Selecciona un subconjunto específico de columnas relevantes para el análisis.
    *   Renombra estas columnas a nombres más descriptivos y amigables para el usuario.

    ```python
    columnas_necesarias = ["_id", "user", "increm[0]", "correo[0]", "Nivel[0][0]", "logs[0].stats[0].value", "logs[0].stats[0].message", "created_at"]
    df = df[columnas_necesarias]

    df = df.rename(columns={
        "logs[0].stats[0].value": "Cantidad Cerebritos",
        "logs[0].stats[0].message": "Razón de Cerebritos",
        "increm[0]": "ID_SIS",
        "correo[0]": "Correo",
        "_id": "ID_Logs",
        "user": "Id_User",
        "Nivel[0][0]": "Grado",
        "created_at": "Fecha"
    })
    ```

3.  **Normalización de Datos (Transform - Normalization):**
    *   Mapea los identificadores internos de los niveles educativos (ej. "6304e6f54ede93101de8c818") a descripciones legibles (ej. "6to Grado").

    ```python
    df['Grado'] = df['Grado'].replace("6304e6f54ede93101de8c818", "6to Grado")
    df['Grado'] = df['Grado'].replace("6304e6ecdff9db10550fabd1", "5to Grado")
    # ... (otras reemplazos de grados)
    ```

4.  **Guardado Intermedio (Load - Intermediate):**
    *   Guarda el DataFrame transformado hasta este punto como `Cerebros_parcial.csv`.

    ```python
    df.to_csv("Cerebros_parcial.csv")
    ```

5.  **Agregación de Datos (Transform - Aggregation):**
    *   Agrupa los datos por `Correo` y `Grado`.
    *   Calcula la suma total de "Cantidad Cerebritos" para cada combinación de `Correo` y `Grado`.

    ```python
    columnas_agrupacion = ["Correo", "Grado"]
    df_agrupado = df.groupby(columnas_agrupacion).agg(
        Total_cerebritos=('Cantidad Cerebritos', 'sum')
    ).reset_index()
    ```

6.  **Guardado Final (Load - Final):**
    *   Guarda el DataFrame agregado como `CSV_AGRUPADO.csv`.
    *   Guarda el DataFrame completo y limpio como `Listado_Completo.csv`.

    ```python
    df_agrupado.to_csv("CSV_AGRUPADO.csv")
    df.to_csv("Listado_Completo.csv")
    ```

## 3. Configuración y Dependencias

### Dependencias del Sistema Operativo

Este script no requiere dependencias a nivel de sistema operativo (ej. FFmpeg, Tesseract, controladores específicos). Su ejecución es independiente de componentes externos más allá del intérprete de Python.

### Dependencias de Python

El script depende exclusivamente de la librería `pandas`.

### Instalación

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2.  **Crear un Entorno Virtual (Recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install pandas
    ```

4.  **Colocar Archivos de Entrada:**
    Asegúrese de que los archivos `Gamificación ago- dic.csv` y `kuepa_sis.gamification_logsDic02-Mar1.csv` estén presentes en el mismo directorio que `main.py`.

5.  **Ejecutar el Script:**
    ```bash
    python main.py
    ```

## 4. Estructura de Salida de Datos

El script genera varios archivos CSV. A continuación, se muestran ejemplos de la estructura de los dos archivos de salida más relevantes para el análisis.

### `Cerebros_parcial.csv`

Este archivo contiene el listado completo de logs de gamificación, con columnas seleccionadas, renombradas y los grados normalizados.

```csv
ID_Logs,Id_User,ID_SIS,Correo,Grado,Cantidad Cerebritos,Razón de Cerebritos,Fecha
65e4d204d80a3a00085a1a1a,6304e6f54ede93101de8c818,12345,usuario1@ejemplo.com,6to Grado,100,Completó Misión A,2023-01-15T10:30:00.000Z
65e4d204d80a3a00085a1a1b,6304e6ecdff9db10550fabd1,67890,usuario2@ejemplo.com,5to Grado,50,Respondió Pregunta,2023-01-15T11:00:00.000Z
65e4d204d80a3a00085a1a1c,6304e6f54ede93101de8c818,12345,usuario1@ejemplo.com,6to Grado,20,Participó en Foro,2023-01-15T11:15:00.000Z
```

### `CSV_AGRUPADO.csv`

Este archivo presenta la suma total de "Cantidad Cerebritos" por cada combinación única de `Correo` y `Grado`, ideal para análisis de rendimiento agregado.

```csv
Correo,Grado,Total_cerebritos
usuario1@ejemplo.com,6to Grado,120
usuario2@ejemplo.com,5to Grado,50
usuario3@ejemplo.com,4to Grado,80
```

## 5. Análisis Técnico y Justificación de Librerías

El script utiliza la librería `pandas` de Python, una herramienta fundamental para la manipulación y análisis de datos tabulares.

*   **`pandas.read_csv()`**: Permite la carga eficiente de datos desde archivos CSV a objetos `DataFrame`, que son la estructura de datos central de `pandas`. Su robustez maneja diversos formatos y opciones de parseo.
*   **`pandas.concat()`**: Esencial para la unificación de datasets. Permite combinar DataFrames a lo largo de un eje específico (en este caso, verticalmente, `axis=0`), lo que es crucial para consolidar logs de diferentes períodos en un único conjunto de datos coherente.
*   **Selección de Columnas (`df[columnas_necesarias]`)**: La notación de indexación de `pandas` facilita la selección precisa de subconjuntos de columnas, eliminando datos irrelevantes y reduciendo la complejidad del DataFrame.
*   **`DataFrame.rename()`**: Permite cambiar los nombres de las columnas de manera programática. Esto es vital para transformar nombres de columnas crípticos o generados automáticamente (ej. `logs[0].stats[0].value`) en etiquetas claras y significativas para el análisis (ej. `Cantidad Cerebritos`).
*   **`Series.replace()`**: Utilizado para la normalización de datos categóricos. En este caso, mapea IDs internos de grados a descripciones legibles por humanos, lo que mejora la interpretabilidad de los datos sin alterar la estructura subyacente.
*   **`DataFrame.groupby().agg().reset_index()`**: Esta secuencia de operaciones es el corazón de la agregación de datos.
    *   `groupby()`: Agrupa el DataFrame por una o más columnas (`Correo`, `Grado`), creando grupos lógicos de filas con valores idénticos en esas columnas.
    *   `agg()`: Aplica una o más funciones de agregación a los grupos. En este caso, se utiliza para calcular la `sum` de `Cantidad Cerebritos`, y se le asigna un nuevo nombre a la columna resultante (`Total_cerebritos`).
    *   `reset_index()`: Convierte las columnas de agrupación de nuevo en columnas regulares del DataFrame, lo que es útil para exportar los resultados a un formato plano como CSV.

La elección de `pandas` se justifica por su rendimiento optimizado para operaciones con grandes volúmenes de datos tabulares, su API intuitiva y su amplia adopción en la comunidad de ciencia de datos, lo que garantiza mantenibilidad y escalabilidad. Su capacidad para manejar datos heterogéneos y realizar transformaciones complejas con pocas líneas de código lo convierte en la herramienta ideal para este tipo de pipeline ETL.

## 6. Valor de Negocio y Aplicaciones

Este script de procesamiento de datos de gamificación ofrece un valor significativo al transformar datos brutos en inteligencia accionable, permitiendo una gestión más estratégica de las iniciativas de engagement.

### Preguntas de Negocio Abordadas

*   ¿Cuál es el nivel de engagement general de los usuarios con el sistema de gamificación?
*   ¿Cómo se distribuyen los "Cerebritos" (puntos de gamificación) entre los diferentes usuarios y grados?
*   ¿Existen diferencias significativas en la participación de gamificación entre los distintos niveles educativos?
*   ¿Qué usuarios son los más activos y cuáles podrían necesitar incentivos adicionales?

### Valor Agregado

El principal valor agregado de este script radica en la **centralización y estandarización de la información de gamificación**. Al consolidar datos de múltiples fuentes y normalizar sus formatos, se elimina la necesidad de procesamiento manual, reduciendo errores y el tiempo de preparación para el análisis. Esto permite a los analistas y gestores de producto enfocarse en la interpretación de los datos en lugar de su limpieza.

### Capacidades de Medición y Diagnóstico

*   **Medición:**
    *   **Total de "Cerebritos" por usuario y grado:** Cuantifica el rendimiento individual y colectivo.
    *   **Frecuencia de logs:** Permite inferir la actividad general de los usuarios.
    *   **Distribución de engagement:** Mide cómo se reparte la participación a través de la base de usuarios y los segmentos educativos.
*   **Diagnóstico:**
    *   **Identificación de brechas de engagement:** Permite detectar qué grados o grupos de usuarios muestran menor actividad, señalando posibles problemas en la relevancia o diseño de la gamificación para esos segmentos.
    *   **Detección de usuarios de alto rendimiento:** Facilita la identificación de "campeones" que pueden servir como modelos o para estudios de caso.
    *   **Análisis de tendencias:** Al consolidar datos a lo largo del tiempo, se pueden diagnosticar cambios en el engagement y la efectividad de las actualizaciones de gamificación.

### Resolución, Optimización y Estandarización

*   **Resuelve:**
    *   **Fragmentación de datos:** Unifica la información de gamificación dispersa en múltiples archivos.
    *   **Inconsistencia de datos:** Normaliza nombres de columnas y valores categóricos (ej. IDs de grados).
    *   **Dificultad de análisis:** Proporciona un dataset limpio y estructurado, listo para herramientas de BI o análisis estadístico.
*   **Optimiza:**
    *   **Tiempo de preparación de datos:** Automatiza un proceso que de otro modo sería manual y propenso a errores.
    *   **Eficiencia del análisis:** Los datos pre-procesados aceleran cualquier análisis posterior.
    *   **Toma de decisiones:** Al tener datos fiables y accesibles, las decisiones sobre la estrategia de gamificación pueden tomarse más rápidamente y con mayor fundamento.
*   **Estandariza:**
    *   **Formato de logs:** Asegura que todos los logs de gamificación sigan una estructura y nomenclatura consistentes.
    *   **Métricas clave:** Define claramente cómo se calculan y presentan las métricas de engagement.

### Oportunidades de Repensar Estrategias

La información generada por este pipeline permite **repensar** fundamentalmente las estrategias de gamificación:

*   **Diseño de Incentivos:** Si un grado específico muestra un bajo total de "Cerebritos", se puede repensar el tipo de actividades gamificadas o recompensas ofrecidas para ese grupo demográfico. Por ejemplo, los estudiantes de grados inferiores podrían responder mejor a recompensas tangibles o actividades más visuales, mientras que los de grados superiores podrían valorar más el reconocimiento o desafíos complejos.
*   **Segmentación de Contenido:** Al entender qué grados son más activos, se puede repensar la segmentación del contenido gamificado, adaptando los desafíos y las narrativas a los intereses y capacidades de cada nivel educativo.
*   **Intervenciones Dirigidas:** Se puede repensar la implementación de intervenciones proactivas para usuarios o grados con bajo engagement, ofreciendo apoyo personalizado o nuevas oportunidades de participación.
*   **Evaluación de Impacto:** La capacidad de medir el total de "Cerebritos" permite evaluar el impacto directo de nuevas características de gamificación o campañas específicas, llevando a un ciclo de mejora continua.
*   **Benchmarking Interno:** Los datos agregados por grado permiten establecer benchmarks internos de engagement, facilitando la identificación de las mejores prácticas entre los diferentes niveles educativos.

En resumen, este script no solo procesa datos, sino que habilita una capa de inteligencia de negocio que permite a la organización diagnosticar el estado actual de su gamificación, optimizar sus procesos y, lo más importante, repensar y evolucionar sus estrategias para maximizar el engagement y el impacto educativo.