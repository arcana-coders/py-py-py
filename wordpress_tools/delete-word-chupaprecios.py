import pandas as pd

# Ruta al archivo CSV original
input_file = 'excel/chupaprecios-otrascategorias-ready.csv'

# Cargar el archivo CSV y eliminar el BOM si está presente
df = pd.read_csv(input_file, encoding='utf-8-sig')

# Función para limpiar las descripciones y eliminar todo después de 'CHUPAPRECIOS'
def limpiar_descripcion(descripcion):
    if isinstance(descripcion, str):  # Verifica si la descripción es una cadena de texto
        if 'CHUPAPRECIOS' in descripcion:
            # Eliminar todo lo que está después de 'CHUPAPRECIOS', incluyendo la palabra
            descripcion = descripcion.split('CHUPAPRECIOS', 1)[0].strip()  # Mantener solo el texto antes de 'CHUPAPRECIOS'
    return descripcion

# Aplicar la función a la columna 'Descripción'
df['Descripción'] = df['Descripción'].apply(limpiar_descripcion)

# Verificar si eliminó correctamente 'CHUPAPRECIOS'
apariciones_chupaprecios = df['Descripción'].str.contains('CHUPAPRECIOS', na=False).sum()

print(f"La palabra 'CHUPAPRECIOS' aparece {apariciones_chupaprecios} veces después de la limpieza.")

# Guardar el archivo procesado para verificar los cambios
output_file = 'excel/chupaprecios-otrascategorias-limpio.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Archivo procesado guardado como: {output_file}")
