import requests
import csv
import random
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup

# Función para agregar retrasos aleatorios
def sleep():
    time.sleep(random.uniform(3, 8))

# Función para extraer los datos de la página de Amazon
def extraer_datos_pagina(url):
    # Configuramos las cabeceras de la solicitud para simular ser un navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers",
    }
    # Realizamos la solicitud HTTP y obtenemos el contenido de la página
    response = requests.get(url, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    
    # Buscamos los datos del producto en la página
    nombre = soup.find("span", {"id": "productTitle"}).text.strip()
    descripcion = soup.find("div", {"id": "productDescription"}).text.strip()
    precio = soup.find("span", {"id": "priceblock_ourprice"}).text.strip()
    asin = soup.find("span", {"class": "product-asin"}).text.strip()
    imagenes = [img["src"] for img in soup.select("#altImages .a-button-image img")]

    return [nombre, descripcion, precio, asin, imagenes]

# Función para extraer los datos de todos los productos en una página de Amazon y agregarlos a un archivo CSV
def extraer_productos_pagina(url, categoria):
    # Configuramos las cabeceras de la solicitud para simular ser un navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers",
    }

    # Extraemos los datos de la página
    response = requests.get(url, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")

    # Buscamos todos los enlaces a los productos en la página
    enlaces = soup.select("a.a-link-normal.s-no-outline")

    # Creamos el nombre del archivo CSV con la fecha y hora actual
    now = datetime.now()
    fecha_hora = now.strftime("%Y-%m-%d %H-%M-%S")
    nombre_archivo = re.sub(r'\W+', '', f"{categoria} {fecha_hora}.csv")

    # Abrimos el archivo CSV para escribir los datos extraídos
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Escribimos la fila de encabezado
        writer.writerow(["Nombre", "Descripción", "Precio", "ASIN", "Imágenes"])

        # Recorremos todos los enlaces a los productos en la página y extraemos los datos de cada producto
        for enlace in enlaces:
            url_producto = "https://www.amazon.com" + enlace["href"]
            datos_producto = extraer_datos_pagina(url_producto)

            # Escribimos los datos del producto en el archivo CSV
            writer.writerow(datos_producto)

            # Agregamos un retraso aleatorio antes de la siguiente solicitud
            sleep()

# URL de la página de Amazon a partir de la cual se extraerán los datos
url_categoria = input("Introduce la URL de la categoría de Amazon: ")

# Extraemos los productos de la página de la categoría y las siguientes páginas
pagina = 1
while True:
    url_pagina = f"{url_categoria}&page={pagina}"
    response = requests.get(url_pagina)
    if response.status_code == 404:
        break
    extraer_productos_pagina(url_pagina, url_categoria.split("/")[-2])
    pagina += 1

print("La información se ha guardado en el archivo CSV correspondiente.") 
