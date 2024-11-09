import os
import pandas as pd

# Este codigo prepara el archivo excel descargado de una categoria en integraly, para subirlo nuevamente a MELI en nuestra tienda.

# Definición de la frase adicional
frase_adicional = """
===================================
CAPALSA tu tienda online
Facturamos si lo requieres
Productos importados legalmente
7 días es el tiempo de entrega
===================================
"""

# Función para limpiar las descripciones y eliminar todo después de 'CHUPAPRECIOS'
def limpiar_descripcion(descripcion):
    if isinstance(descripcion, str):  # Verifica si la descripción es una cadena de texto
        if 'CHUPAPRECIOS' in descripcion:
            # Eliminar todo lo que está después de 'CHUPAPRECIOS', incluyendo la palabra
            descripcion = descripcion.split('CHUPAPRECIOS', 1)[0].strip()  # Mantener solo el texto antes de 'CHUPAPRECIOS'
    return descripcion

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

def cargar_archivo():
    # Bucle para solicitar la ruta hasta que se encuentre el archivo
    while True:
        archivo_excel = input("Por favor, introduce la ruta del archivo Excel: ")
        if os.path.isfile(archivo_excel):
            print(f"Archivo encontrado: {archivo_excel}")
            return archivo_excel
        else:
            print("Archivo no encontrado. Por favor, inténtalo de nuevo.")

def procesar_datos(archivo_excel):
    # Cargar el archivo Excel en un DataFrame
    df = pd.read_excel(archivo_excel, engine='openpyxl')

    # Limpiar los nombres de las columnas
    df.columns = df.columns.str.replace(r'[\n\r]', '', regex=True).str.replace(r'_x000D_', '', regex=True).str.strip()

    # Filtrar solo productos cuya 'Moneda' sea 'MXN'
    df = df[df['Moneda'] == 'MXN']

    # Limpiar la columna 'Moneda' y renombrar columnas
    df['Moneda'] = ''  # Vaciar el contenido de la columna
    df = df.rename(columns={'Precio': 'Proveedor', 'Moneda': 'Precio'})

    # Aplicar la función para modificar el precio en la columna 'Precio' basada en 'Proveedor'
    df['Precio'] = df['Proveedor'].apply(modificar_precio)

    # Limpiar y modificar la columna 'Descripción' si existe
    if 'Descripción' in df.columns:
        df['Descripción'] = df['Descripción'].apply(limpiar_descripcion)
        
        # Añadir la frase adicional a la descripción de cada producto
        df['Descripción'] = frase_adicional + '\n' + df['Descripción'].astype(str)

    # Ordenar por 'Vendidos' (descendente) y luego 'Visitas' (descendente)
    df['Vendidos'] = df['Vendidos'].astype(str).str.extract(r'(\d+)', expand=False).fillna(0).astype(int)
    df = df.sort_values(by=['Vendidos', 'Visitas'], ascending=[False, False])

    # Filtrar filas que tienen vendidos o más de 1000 visitas
    df_filtrado = df[(df['Vendidos'] > 0) | (df['Visitas'] > 1000)]

    # Filtrar filas con disponibilidad de stock mayor a 0, el tiempo para tener el producto
    if 'Disponibilidad de stock' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['Disponibilidad de stock'].fillna(0) > 0]

    # Generar el nombre del nuevo archivo con la palabra "modificado"
    ruta, nombre_archivo = os.path.split(archivo_excel)
    nombre_modificado = nombre_archivo.replace('.xlsx', '-modificado.xlsx')
    archivo_modificado = os.path.join(ruta, nombre_modificado)

    # Guardar el resultado en un nuevo archivo Excel
    df_filtrado.to_excel(archivo_modificado, index=False, engine='openpyxl')
    print(f"Proceso completado y archivo guardado como '{archivo_modificado}'")

def main():
    archivo_excel = cargar_archivo()
    procesar_datos(archivo_excel)

# Llamar a la función principal
main()
