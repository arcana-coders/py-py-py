from datetime import datetime
import pandas as pd
import os

# Ruta al archivo CSV original
input_file = 'excel/181024-importasimple-belleza+industrias-filtrado.csv'
# "C:\Users\Capalsa\Desktop\python-meli-ds\excel\130124-importasimple-tercero-filtrado.csv"

# Cargar el archivo CSV y eliminar el BOM si está presente
df = pd.read_csv(input_file, encoding='utf-8-sig')
print(df.columns)

# Verificar cómo se ve la columna 'Descripción' antes de cualquier modificación
print("Muestra de 'Descripción' antes de limpiar:")
print(df['Descripción'].head(5))

# Asegurarse de que solo se aplica strip a las cadenas de texto en 'Proveedor'
df['Proveedor'] = df['Proveedor'].apply(lambda x: x.strip() if isinstance(x, str) else x)

# Eliminar los símbolos de $ y comas en 'Proveedor'
df['Proveedor'] = df['Proveedor'].replace({'$': '', ',': ''}, regex=True)  # Elimina símbolos de $ y comas

# Convertir la columna 'Proveedor' a tipo float
df['Proveedor'] = pd.to_numeric(df['Proveedor'], errors='coerce')  # Convierte a tipo float y fuerza NaN en errores

# Función para modificar el precio basado en el valor de 'Proveedor'
def modificar_precio(proveedor):
    if pd.isna(proveedor):  # Manejar valores NaN
        return proveedor  # Si es NaN, no modificar el valor
    if 99 <= proveedor <= 1998:
        return proveedor - 50
    elif 1999 <= proveedor <= 4999:
        return proveedor - 100
    elif 5000 <= proveedor <= 9999:
        return proveedor - 300
    elif 10000 <= proveedor <= 19999:
        return proveedor - 800
    else:
        return proveedor  # Si no cae en ninguno de los rangos, no modifica el precio

# Aplicar la función a la columna 'Precio'
df['Precio'] = df['Proveedor'].apply(modificar_precio)

# Modificar las categorías para quedarse solo con la principal
df['Categoría'] = df['Categoría'].apply(lambda x: x.split(' > ')[0] if isinstance(x, str) else x)

# Combinar todas las columnas de imágenes en una sola columna, separadas por comas
image_columns = ['Imagen 1', 'Imagen 2', 'Imagen 3', 'Imagen 4', 'Imagen 5', 'Imagen 6', 'Imagen 7', 'Imagen 8', 'Imagen 9', 'Imagen 10']
df['Imagenes'] = df[image_columns].apply(lambda row: ','.join(row.dropna()), axis=1)

# Eliminar las columnas individuales de imágenes
df_cleaned = df.drop(columns=image_columns)

# Función para limpiar las descripciones y eliminar todo después de 'CHUPAPRECIOS'
def limpiar_descripcion(descripcion):
    if isinstance(descripcion, str):  # Verifica si la descripción es una cadena de texto
        if 'CHUPAPRECIOS' in descripcion:
            # Eliminar todo lo que está después de 'CHUPAPRECIOS', incluyendo la palabra
            descripcion = descripcion.split('CHUPAPRECIOS', 1)[0].strip()  # Mantener solo el texto antes de 'CHUPAPRECIOS'
    return descripcion

# Aplicar la función a la columna 'Descripción'
df_cleaned['Descripción'] = df_cleaned['Descripción'].apply(limpiar_descripcion)

# Verificar si eliminó correctamente 'CHUPAPRECIOS'
apariciones_chupaprecios = df_cleaned['Descripción'].str.contains('CHUPAPRECIOS', na=False).sum()

print(f"La palabra 'CHUPAPRECIOS' aparece {apariciones_chupaprecios} veces después de la limpieza.")
print("Muestra de 'Descripción' después de limpiar:")
print(df_cleaned['Descripción'].head(5))

# Añadir la frase a la descripción de cada producto
frase_adicional = """
===================================
CAPALSA tu tienda online
Facturamos si lo requieres
Productos importados legalmente
7 días es el tiempo de entrega
===================================
"""
df_cleaned['Descripción'] = frase_adicional + '\n' + df_cleaned['Descripción']

# Obtener el nombre original del archivo sin la extensión
original_filename = os.path.splitext(input_file)[0]

# Obtener la fecha y hora actual
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Crear el nombre del archivo de salida sumando la fecha y hora al original
output_file = f"{original_filename}_{current_time}.csv"

# Guardar el archivo con comillas para manejar las comas correctamente en Excel
df_cleaned.to_csv(output_file, index=False, encoding='utf-8-sig', quoting=1)

print(f"Archivo procesado guardado como: {output_file}")
