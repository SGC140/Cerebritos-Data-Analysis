import pandas as pd

data1 = pd.read_csv("Gamificación ago- dic.csv")
data2 = pd.read_csv("kuepa_sis.gamification_logsDic02-Mar1.csv")
data = pd.concat([data1, data2])
data.to_csv("cerebritos.csv")

df = data

print(df.columns.to_list())

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

df['Grado'] = df['Grado'].replace("6304e6f54ede93101de8c818", "6to Grado")
df['Grado'] = df['Grado'].replace("6304e6ecdff9db10550fabd1", "5to Grado")
df['Grado'] = df['Grado'].replace("6304e6e6766c140ffb1ca932", "4to Grado")
df['Grado'] = df['Grado'].replace("6304e6dedff9db10550fa9d6", "3to Grado")
df['Grado'] = df['Grado'].replace("6304e6d4766c140ffb1ca8f8", "2to Grado")
df['Grado'] = df['Grado'].replace("6304e6cbdff9db10550fa6e0", "1to Grado")

print(df.columns.to_list())

df.to_csv("Cerebros_parcial.csv")

conteos_correo = df['Correo'].value_counts()
print(conteos_correo)

columnas_agrupacion = ["Correo", "Grado"]

df_agrupado = df.groupby(columnas_agrupacion).agg(
    Total_cerebritos=('Cantidad Cerebritos', 'sum')
).reset_index()

df_agrupado = pd.DataFrame(df_agrupado)

df_agrupado.to_csv("CSV_AGRUPADO.csv")
df.to_csv("Listado_Completo.csv")