# Gamification Log Processing and Aggregation

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![License](https://img.shields.io/badge/License-Proprietary-blue)

This repository contains a Python script designed to consolidate, clean, and aggregate gamification log data from multiple CSV sources. The main objective is to transform raw, fragmented data into a structured and analyzable format, facilitating the measurement of user engagement and performance by educational level.

## Table of Contents

1.  [Project Overview](#1-project-overview)
2.  [Pipeline Architecture and Logic](#2-pipeline-architecture-and-logic)
    *   [Input Payload](#input-payload)
    *   [Pipeline Flow](#pipeline-flow)
3.  [Setup and Dependencies](#3-setup-and-dependencies)
    *   [Operating System Dependencies](#operating-system-dependencies)
    *   [Python Dependencies](#python-dependencies)
    *   [Installation](#installation)
4.  [Data Output Structure](#4-data-output-structure)
    *   [Cerebros_parcial.csv](#cerebros_parcialcsv)
    *   [CSV_AGRUPADO.csv](#csv_agrupado.csv)
5.  [Technical Analysis and Library Justification](#5-technical-analysis-and-library-justification)
6.  [Business Value and Applications](#6-business-value-and-applications)
    *   [Business Questions Addressed](#business-questions-addressed)
    *   [Added Value](#added-value)
    *   [Measurement and Diagnostic Capabilities](#measurement-and-diagnostic-capabilities)
    *   [Resolution, Optimization, and Standardization](#resolution-optimization-and-standardization)
    *   [Opportunities to Rethink Strategies](#opportunities-to-rethink-strategies)

---

## 1. Project Overview

This project addresses the need to consolidate and standardize gamification data scattered across multiple CSV files. The `main.py` script automates the merging of these datasets, the selection and renaming of key columns, the normalization of educational level identifiers, and the aggregation of engagement metrics. The result is a clean, analysis-ready dataset that allows for a deep understanding of user behavior within the gamification system.

## 2. Pipeline Architecture and Logic

The project's architecture is an ETL (Extract, Transform, Load) type, based on a monolithic Python script.

### Input Payload

The pipeline requires two input CSV files located in the same directory as the `main.py` script:

*   `Gamificación ago- dic.csv`: Contains gamification logs from an initial period.
*   `kuepa_sis.gamification_logsDic02-Mar1.csv`: Contains gamification logs from a later period.

Both files must contain columns that allow for the extraction of `_id`, `user`, `increm[0]`, `correo[0]`, `Nivel[0][0]`, `logs[0].stats[0].value`, `logs[0].stats[0].message`, and `created_at`.

### Pipeline Flow

The `main.py` script executes the following sequence of operations:

1.  **Extraction and Consolidation (Extract & Concatenate):**
    *   Loads `Gamificación ago- dic.csv` and `kuepa_sis.gamification_logsDic02-Mar1.csv` into Pandas DataFrames.
    *   Concatenates both DataFrames vertically to create a unified dataset.
    *   Saves the initial consolidated dataset as `cerebritos.csv`.

    ```python
    import pandas as pd

    data1 = pd.read_csv("Gamificación ago- dic.csv")
    data2 = pd.read_csv("kuepa_sis.gamification_logsDic02-Mar1.csv")
    data = pd.concat([data1, data2])
    data.to_csv("cerebritos.csv")
    ```

2.  **Column Selection and Renaming (Transform - Selection & Renaming):**
    *   Selects a specific subset of columns relevant for analysis.
    *   Renames these columns to more descriptive and user-friendly names.

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

3.  **Data Normalization (Transform - Normalization):**
    *   Maps internal educational level identifiers (e.g., "6304e6f54ede93101de8c818") to readable descriptions (e.g., "6to Grado").

    ```python
    df['Grado'] = df['Grado'].replace("6304e6f54ede93101de8c818", "6to Grado")
    df['Grado'] = df['Grado'].replace("6304e6ecdff9db10550fabd1", "5to Grado")
    # ... (other grade replacements)
    ```

4.  **Intermediate Save (Load - Intermediate):**
    *   Saves the DataFrame transformed up to this point as `Cerebros_parcial.csv`.

    ```python
    df.to_csv("Cerebros_parcial.csv")
    ```

5.  **Data Aggregation (Transform - Aggregation):**
    *   Groups the data by `Correo` and `Grado`.
    *   Calculates the total sum of "Cantidad Cerebritos" for each `Correo` and `Grado` combination.

    ```python
    columnas_agrupacion = ["Correo", "Grado"]
    df_agrupado = df.groupby(columnas_agrupacion).agg(
        Total_cerebritos=('Cantidad Cerebritos', 'sum')
    ).reset_index()
    ```

6.  **Final Save (Load - Final):**
    *   Saves the aggregated DataFrame as `CSV_AGRUPADO.csv`.
    *   Saves the complete and clean DataFrame as `Listado_Completo.csv`.

    ```python
    df_agrupado.to_csv("CSV_AGRUPADO.csv")
    df.to_csv("Listado_Completo.csv")
    ```

## 3. Setup and Dependencies

### Operating System Dependencies

This script does not require operating system-level dependencies (e.g., FFmpeg, Tesseract, specific drivers). Its execution is independent of external components beyond the Python interpreter.

### Python Dependencies

The script exclusively depends on the `pandas` library.

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install pandas
    ```

4.  **Place Input Files:**
    Ensure that the `Gamificación ago- dic.csv` and `kuepa_sis.gamification_logsDic02-Mar1.csv` files are present in the same directory as `main.py`.

5.  **Run the Script:**
    ```bash
    python main.py
    ```

## 4. Data Output Structure

The script generates several CSV files. Below are examples of the structure of the two most relevant output files for analysis.

### `Cerebros_parcial.csv`

This file contains the complete list of gamification logs, with selected, renamed columns and normalized grades.

```csv
ID_Logs,Id_User,ID_SIS,Correo,Grado,Cantidad Cerebritos,Razón de Cerebritos,Fecha
65e4d204d80a3a00085a1a1a,6304e6f54ede93101de8c818,12345,usuario1@ejemplo.com,6to Grado,100,Completó Misión A,2023-01-15T10:30:00.000Z
65e4d204d80a3a00085a1a1b,6304e6ecdff9db10550fabd1,67890,usuario2@ejemplo.com,5to Grado,50,Respondió Pregunta,2023-01-15T11:00:00.000Z
65e4d204d80a3a00085a1a1c,6304e6f54ede93101de8c818,12345,usuario1@ejemplo.com,6to Grado,20,Participó en Foro,2023-01-15T11:15:00.000Z
```

### `CSV_AGRUPADO.csv`

This file presents the total sum of "Cantidad Cerebritos" for each unique combination of `Correo` and `Grado`, ideal for aggregated performance analysis.

```csv
Correo,Grado,Total_cerebritos
usuario1@ejemplo.com,6to Grado,120
usuario2@ejemplo.com,5to Grado,50
usuario3@ejemplo.com,4to Grado,80
```

## 5. Technical Analysis and Library Justification

The script uses the `pandas` Python library, a fundamental tool for tabular data manipulation and analysis.

*   **`pandas.read_csv()`**: Allows for efficient data loading from CSV files into `DataFrame` objects, which are the core data structure of `pandas`. Its robustness handles various formats and parsing options.
*   **`pandas.concat()`**: Essential for dataset unification. It allows combining DataFrames along a specific axis (in this case, vertically, `axis=0`), which is crucial for consolidating logs from different periods into a single coherent dataset.
*   **Column Selection (`df[columnas_necesarias]`)**: Pandas' indexing notation facilitates the precise selection of column subsets, eliminating irrelevant data and reducing DataFrame complexity.
*   **`DataFrame.rename()`**: Allows programmatic renaming of columns. This is vital for transforming cryptic or automatically generated column names (e.g., `logs[0].stats[0].value`) into clear and meaningful labels for analysis (e.g., `Cantidad Cerebritos`).
*   **`Series.replace()`**: Used for categorical data normalization. In this case, it maps internal grade IDs to human-readable descriptions, which improves data interpretability without altering the underlying structure.
*   **`DataFrame.groupby().agg().reset_index()`**: This sequence of operations is the core of data aggregation.
    *   `groupby()`: Groups the DataFrame by one or more columns (`Correo`, `Grado`), creating logical groups of rows with identical values in those columns.
    *   `agg()`: Applies one or more aggregation functions to the groups. In this case, it is used to calculate the `sum` of `Cantidad Cerebritos`, and the resulting column is assigned a new name (`Total_cerebritos`).
    *   `reset_index()`: Converts the grouping columns back into regular DataFrame columns, which is useful for exporting results to a flat format like CSV.

The choice of `pandas` is justified by its optimized performance for operations with large volumes of tabular data, its intuitive API, and its widespread adoption in the data science community, which ensures maintainability and scalability. Its ability to handle heterogeneous data and perform complex transformations with few lines of code makes it the ideal tool for this type of ETL pipeline.

## 6. Business Value and Applications

This gamification data processing script offers significant value by transforming raw data into actionable intelligence, enabling more strategic management of engagement initiatives.

### Business Questions Addressed

*   What is the overall engagement level of users with the gamification system?
*   How are "Cerebritos" (gamification points) distributed among different users and grades?
*   Are there significant differences in gamification participation across different educational levels?
*   Which users are the most active, and which might need additional incentives?

### Added Value

The main added value of this script lies in the **centralization and standardization of gamification information**. By consolidating data from multiple sources and normalizing their formats, the need for manual processing is eliminated, reducing errors and preparation time for analysis. This allows analysts and product managers to focus on data interpretation rather than data cleaning.

### Measurement and Diagnostic Capabilities

*   **Measurement:**
    *   **Total "Cerebritos" per user and grade:** Quantifies individual and collective performance.
    *   **Log frequency:** Allows inferring overall user activity.
    *   **Engagement distribution:** Measures how participation is spread across the user base and educational segments.
*   **Diagnosis:**
    *   **Identification of engagement gaps:** Allows detecting which grades or user groups show less activity, pointing to potential issues in the relevance or design of gamification for those segments.
    *   **Detection of high-performing users:** Facilitates the identification of "champions" who can serve as role models or for case studies.
    *   **Trend analysis:** By consolidating data over time, changes in engagement and the effectiveness of gamification updates can be diagnosed.

### Resolution, Optimization, and Standardization

*   **Resolves:**
    *   **Data fragmentation:** Unifies gamification information scattered across multiple files.
    *   **Data inconsistency:** Normalizes column names and categorical values (e.g., grade IDs).
    *   **Analysis difficulty:** Provides a clean and structured dataset, ready for BI tools or statistical analysis.
*   **Optimizes:**
    *   **Data preparation time:** Automates a process that would otherwise be manual and error-prone.
    *   **Analysis efficiency:** Pre-processed data accelerates any subsequent analysis.
    *   **Decision-making:** By having reliable and accessible data, decisions about gamification strategy can be made more quickly and with greater foundation.
*   **Standardizes:**
    *   **Log format:** Ensures that all gamification logs follow a consistent structure and nomenclature.
    *   **Key metrics:** Clearly defines how engagement metrics are calculated and presented.

### Opportunities to Rethink Strategies

The information generated by this pipeline allows for a fundamental **rethinking** of gamification strategies:

*   **Incentive Design:** If a specific grade shows a low total of "Cerebritos", the type of gamified activities or rewards offered for that demographic group can be rethought. For example, students in lower grades might respond better to tangible rewards or more visual activities, while those in higher grades might value recognition or complex challenges more.
*   **Content Segmentation:** By understanding which grades are most active, the segmentation of gamified content can be rethought, adapting challenges and narratives to the interests and capabilities of each educational level.
*   **Targeted Interventions:** The implementation of proactive interventions for users or grades with low engagement can be rethought, offering personalized support or new participation opportunities.
*   **Impact Evaluation:** The ability to measure the total "Cerebritos" allows for the direct evaluation of the impact of new gamification features or specific campaigns, leading to a continuous improvement cycle.
*   **Internal Benchmarking:** Grade-aggregated data allows for the establishment of internal engagement benchmarks, facilitating the identification of best practices across different educational levels.

In summary, this script not only processes data but also enables a layer of business intelligence that allows the organization to diagnose the current state of its gamification, optimize its processes, and, most importantly, rethink and evolve its strategies to maximize engagement and educational impact.