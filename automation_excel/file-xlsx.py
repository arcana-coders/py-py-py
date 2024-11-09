import pandas as pd

# Cargar el archivo Excel en un DataFrame
archivo_excel = 'excel/181024-importasimple-belleza+industrias-full.xlsx'
# "C:\Users\Capalsa\Desktop\python-meli-ds\excel\181024-importasimple-artepapel-full.xlsx"


df = pd.read_excel(archivo_excel, engine='openpyxl')

# Limpiar los nombres de las columnas
df.columns = df.columns.str.replace(r'[\n\r]', '', regex=True).str.replace(r'_x000D_', '', regex=True).str.strip()

# Ordenar por 'Vendidos' (descendente) y luego 'Visitas' (descendente)
df['Vendidos'] = df['Vendidos'].astype(str).str.extract(r'(\d+)', expand=False).fillna(0).astype(int)
df = df.sort_values(by=['Vendidos', 'Visitas'], ascending=[False, False])

# Filtrar filas que tienen vendidos o más de 1000 visitas
df_filtrado = df[(df['Vendidos'] > 0) | (df['Visitas'] > 1000)]

# Filtrar filas con disponibilidad de stock mayor a 0
if 'Disponibilidad de stock' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Disponibilidad de stock'].fillna(0) > 0]

# Guardar el resultado en un nuevo archivo Excel
df_filtrado.to_excel('excel/181024-importasimple-belleza+industrias-filtrado.xlsx', index=False, engine='openpyxl')

print("Proceso completado y archivo guardado como 'archivo_filtrado_limpio.xlsx'")






