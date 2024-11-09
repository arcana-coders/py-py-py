from pathlib import Path
from colorama import Fore, Style, init

# Inicializar colorama
init()

# Directorio donde buscar
directorio = Path(r'F:\amazon_capalsa')

# Nombre o patrón que buscas en el nombre del archivo
patron = input("¿Qué quieres buscar? ").lower()  # Convertir el patrón a minúsculas

# Carpetas a excluir
excluir_carpetas = [r'F:\amazon_capalsa\compras-img', r'F:\amazon_capalsa\zerobytes']

# Lista para almacenar los archivos encontrados
archivos_encontrados = []

# Variables para manejar el cambio de color por carpeta
colores = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA]
color_actual = None
ultima_carpeta = None
color_index = 0  # Usaremos un índice para recorrer los colores

# Recorrer los archivos en el directorio y sus subdirectorios
for archivo in directorio.rglob('*'):
    # Convertir la ruta del archivo a string y verificar si contiene alguna de las carpetas excluidas
    if any(excluida in str(archivo) for excluida in excluir_carpetas):
        continue

    # Buscar archivos cuyo nombre contenga el patrón sin distinción de mayúsculas o minúsculas
    if patron in archivo.name.lower():  # Convertir el nombre del archivo a minúsculas
        archivos_encontrados.append(archivo)  # Agregar el archivo encontrado a la lista

# Generar el reporte
if archivos_encontrados:
    print(f"\nSe encontraron {len(archivos_encontrados)} archivo(s):")
    for archivo in archivos_encontrados:
        carpeta_actual = archivo.parent
        # Si es una nueva carpeta, cambia el color
        if carpeta_actual != ultima_carpeta:
            color_actual = colores[color_index % len(colores)]
            color_index += 1
            ultima_carpeta = carpeta_actual

        # Imprimir archivo con el color asignado
        print(f"{color_actual}{archivo}{Style.RESET_ALL}")
else:
    print("\nNo se encontró ningún archivo que coincida con el patrón.\n")
