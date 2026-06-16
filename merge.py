import pandas as pd
import os

cerebritos = pd.read_csv("Reporte_cerebros_IQS.csv")
info_usuario = pd.read_csv("bq-results-20260612-141807-1781273916354 - bq-results-20260612-141807-1781273916354.csv")
print(info_usuario)

columnas_editables = ['Centro_Faro', 'Provincia', 'Distrito', 'incremental', 'PROFILE_CELL_PHONE']
columnas_totales = ['Centro_Faro', 'Provincia', 'Distrito', 'incremental', 'PROFILE_CELL_PHONE', 'full_name']


info_usuario = info_usuario[columnas_totales]
info_usuario['incremental'] = info_usuario['incremental'].astype('Int64')
columnas_split = ['Provincia', 'Distrito']

info_usuario[columnas_split] = info_usuario[columnas_split].apply(lambda col: col.str.split("-").str[1].str.strip().fillna("SIN INFORMACIÓN"))
info_usuario['Centro_Faro'] = info_usuario['Centro_Faro'].fillna("SIN INFORMACIÓN") 
info_usuario[columnas_editables] = info_usuario[columnas_editables].replace(
    r'^\s*$', 
    "SIN INFORMACIÓN", 
    regex=True
)
info_usuario['PROFILE_CELL_PHONE'] = info_usuario['PROFILE_CELL_PHONE'].replace(" ", "").replace("-", "").replace("(", "").replace(")", "").str.strip()
info_usuario = info_usuario.drop_duplicates(subset=['incremental'])
print(info_usuario)

df = pd.merge(
    left=cerebritos,
    right=info_usuario,
    how="left",
    left_on='ID',
    right_on='incremental'
)

df = df.drop(columns=['incremental'])
df = df.rename(columns={'value': 'Número de Cerebritos', 
                        'Centro_Faro': 'Centro Educativo',
                        'Provincia': 'Regional',
                        'PROFILE_CELL_PHONE': 'Teléfono',
                        'full_name': 'Nombre Completo'})

columnas_limpieza = ['Nombre Completo', 'Número de Cerebritos', 'Centro Educativo', 'Regional', 'Teléfono', 'Distrito']

df[columnas_limpieza] = df[columnas_limpieza].fillna("SIN INFORMACIÓN")
df = df.drop(columns='Nombre')
print(df)

df.to_csv("Cerebritos_IQS_16_06_2026.csv", index=False)