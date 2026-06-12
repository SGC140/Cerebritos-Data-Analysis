import pandas as pd
import os

cerebritos = pd.read_csv("resultados_iqs_1206.csv")
info_usuario = pd.read_csv("bq-results-20260612-141807-1781273916354 - bq-results-20260612-141807-1781273916354.csv")

columnas_necesarias = ['Centro_Faro', 'Provincia', 'Distrito', 'incremental', 'PROFILE_CELL_PHONE']

info_usuario = info_usuario[columnas_necesarias]
info_usuario['incremental'] = info_usuario['incremental'].astype('Int64')
columnas_split = ['Provincia', 'Distrito']

info_usuario[columnas_split] = info_usuario[columnas_split].apply(lambda col: col.str.split("-").str[1].str.strip().fillna("SIN INFORMACIÓN"))
info_usuario['Centro_Faro'] = info_usuario['Centro_Faro'].fillna("SIN INFORMACIÓN") 
info_usuario = info_usuario.drop_duplicates(subset=['incremental'])

df = pd.merge(
    left=cerebritos,
    right=info_usuario,
    how="left",
    left_on='ID',
    right_on='incremental'
)

df = df.drop(columns=['incremental'])
df = df.rename(columns={'value': 'Número de Cerebritos', 
                        'Centro_faro': 'Centro Educativo',
                        'Provincia': 'Regional',
                        'PROFILE_CELL_PHONE': 'Teléfono'})

df.to_csv("Cerebritos_IQS.csv", index=False)