import csv
import os
import random
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

#Scrapea los links de un link dado, el link dado ya trae filtrado por ranking y por precio
#Guarda los links en un archivo csv, y extrae los links avanzando en paginacion.

# Credenciales de la API
api_key = "c9c5725ddfa15759e306c456463f24b4"

# Solicitamos al usuario que proporcione la URL
url = input("Por favor, introduzca la URL del sitio web: ")

# Preparamos el nombre del archivo
now = datetime.now() 
filename = f"C:\\iherb\\i-herb_{now.strftime('%Y%m%d%H%M%S')}.csv"

# Inicializamos la URL de la siguiente página
next_page_url = url

while next_page_url:
    print("Preparando para raspar la página...")

    # Construimos la URL de la API
    api_url = f"https://api.scraperapi.com?api_key={api_key}&url={next_page_url}"
    print(f"URL de la API construida, realizando la solicitud a {api_url}...")

    # Obtenemos el contenido de la página web a través de la API
    response = requests.get(api_url)
    print("Solicitud completada, analizando el contenido de la página...")

    # Creamos un objeto BeautifulSoup con el contenido de la página web
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscamos los divs con los productos y extraemos los enlaces únicos
    print("Buscando divs con la clase 'products product-cells clearfix'...")
    product_links = set()  # Usamos un conjunto para evitar duplicados
    for div in soup.find_all('div', {'class': 'products product-cells clearfix'}):
        for a in div.find_all('a', href=True):
            product_links.add(a['href'])

    # Guardamos los enlaces en el archivo CSV
    print("Extrayendo enlaces y guardando en el CSV...")
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for link in product_links:
            writer.writerow([link])

    print("Enlaces guardados en el CSV.")

    # Buscamos el enlace de la próxima página
    next_page = soup.find('a', {'class': 'pagination-next'}, href=True)
    next_page_url = next_page['href'] if next_page else None
    print(f"Enlace de la próxima página: {next_page_url}")

    # Esperamos un tiempo aleatorio antes de raspar la próxima página
    wait_time = random.randint(3, 8)
    print(f"Esperando {wait_time} segundos antes de raspar la próxima página...")
    time.sleep(wait_time)

print("Raspado completado.")
