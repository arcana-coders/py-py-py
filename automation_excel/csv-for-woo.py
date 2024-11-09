import pandas as pd

# Ruta al archivo CSV original
input_file = 'excel/MAZMER-ready.csv'

# Carga el archivo CSV con la codificación adecuada (ISO-8859-1 o Latin-1)
df = pd.read_csv(input_file, encoding='utf-8-sig')
print(df.columns)


# 1. Modificar las categorías para quedarse solo con la principal
df['Categoría'] = df['Categoría'].apply(lambda x: x.split(' > ')[0])

# 2. Combinar todas las columnas de imágenes en una sola columna, separadas por comas
image_columns = ['Imagen 1', 'Imagen 2', 'Imagen 3', 'Imagen 4', 'Imagen 5', 'Imagen 6', 'Imagen 7', 'Imagen 8', 'Imagen 9', 'Imagen 10']
df['Imagenes'] = df[image_columns].apply(lambda row: ','.join(row.dropna()), axis=1)

# 3. Eliminar las columnas individuales de imágenes (opcional)
df_cleaned = df.drop(columns=image_columns)

# 4. Añadir la frase a la descripción de cada producto
frase_adicional = """
===================================
===================================
CAPALSA tu tienda online
Facturamos si lo requieres
Productos importados legalmente
7 días es el tiempo de entrega
===================================
===================================
"""
df_cleaned['Descripción'] = frase_adicional + '\n' + df_cleaned['Descripción']

# 5. Guardar el archivo con la codificación correcta para conservar los acentos
output_file = 'excel/MAZMER-ready-cleaned-with-description.csv'
df_cleaned.to_csv(output_file, index=False, encoding='utf-8-sig', quoting=1)

print(f"Archivo procesado guardado como: {output_file}")
