import requests
from bs4 import BeautifulSoup
import time
import random
from termcolor import colored
from colorama import init, Fore, Style
import re
from googletrans import Translator
import csv
from datetime import datetime
import os
import math



init(autoreset=True)

portada = Fore.LIGHTYELLOW_EX + """
 ██████╗ █████╗ ██████╗  █████╗ ██╗    ███████╗ █████╗ 
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║    ██╔════╝██╔══██╗
██║     ███████║██████╔╝███████║██║    ███████╗███████║
██║     ██╔══██║██╔═══╝ ██╔══██║██║       ══██╗██╔══██║
╚██████╗██║  ██║██║     ██║  ██║╚█████╗╚██████╔██║  ██║
 ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═════╝ ╚═════╝╚═╝  ╚═╝
                                                 Coders.
"""

saludo = Fore.GREEN + ('Mayo del 2023, vamos a escrappear nuevamente!')

print(portada)
print(saludo)

# Esta parte extrae los asins del link dado. Pero se asegura de que haya buena conexion y si no lo vuelve a intentar. Genera una lista y la imprime en pantalla.
def get_asins_from_page(url):
    api_key = "c9c5725ddfa15759e306c456463f24b4"
    api_url = f"https://api.scraperapi.com?api_key={api_key}&url={url}"
            
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Referer": "https://www.google.com/",
        "Accept-Language": "es-ES,es;q=0.9"
        }
            
    response = requests.get(api_url, headers=headers)
    
    while response.status_code != 200:
        print(colored(f"Respuesta no exitosa, estado: {response.status_code}. Reintentando...", 'red'))
        time.sleep(random.randint(3, 8))
        response = requests.get(api_url, headers=headers)  # Nota: aquí deberías usar 'api_url' en lugar de 'url'

    print(colored(f"Conexión exitosa, estado: {response.status_code}", 'green'))
    
    soup = BeautifulSoup(response.content, 'html.parser')

    asins = []
    for product_link in soup.find_all('a'):
        href = product_link.get('href')
        if href and '/dp/' in href:
            asin = href.split('/dp/')[1].split('/')[0].split('?')[0]
            asins.append(asin)

    # Si no se encontraron ASINs de esa manera, busca en el atributo 'data-asin' de las etiquetas <div>
    if not asins:
        for div in soup.find_all('div', {'data-asin': True}):
            asin = div.get('data-asin')
            asins.append(asin)
            
    return asins
    pass


def get_product_info(url):
    while True:
        try:
            api_key = "c9c5725ddfa15759e306c456463f24b4"
            api_url = f"https://api.scraperapi.com?api_key={api_key}&url={url}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
                "Referer": "https://www.google.com/",
                "Accept-Language": "es-ES,es;q=0.9"
            }
            
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                print("Conexión exitosa, estado: 200")
                soup = BeautifulSoup(response.text, 'lxml')
                
                translator = Translator()

                # Obteniendo el título
                titulo_element = soup.find("span", {"id": 'productTitle'})
                titulo = titulo_element.string.strip() if titulo_element else "Título no encontrado"
                try:
                    titulo = translator.translate(titulo, src='en', dest='es').text
                except Exception as e:
                    print(f"Error al traducir el título: {e}")

                # Obteniendo las imágenes
                imagenes = []
                div_imagenes = soup.find("div", {"id": "altImages"})
                if div_imagenes is not None:
                    imagen_elements = div_imagenes.find_all("img")
                    for imagen_element in imagen_elements:
                        if len(imagenes) == 3:
                            break
                        imagen_url = imagen_element.get("src").replace('US40', 'SX679')
                        imagenes_str = ','.join(imagen_url)
                        imagenes.append(imagenes_str)

                # Obteniendo la descripción
                descripcion_element = soup.find("div", {"id": 'feature-bullets'})
                if descripcion_element is None:
                    descripcion_element = soup.find("div", {"id": 'aplus'})
                descripcion = descripcion_element.text.strip() if descripcion_element else "Descripción no encontrada"
                try:
                    if descripcion != "Descripción no encontrada":
                        descripcion = translator.translate(descripcion, src='en', dest='es').text
                except Exception as e:
                    print(f"Error al traducir la descripción: {e}")
                
                # Obteniendo el precio
                precio_element_1 = soup.find("span", {"class": 'a-price a-text-price a-size-medium apexPriceToPay'})
                precio_element_2 = soup.find("span", {"class": 'a-price a-text-price header-price a-size-base a-text-normal'})

                if precio_element_1 is not None:
                    precio = precio_element_1.find("span", {"class": 'a-offscreen'}).text.strip()
                elif precio_element_2 is not None:
                    precio = precio_element_2.find("span", {"class": 'a-offscreen'}).text.strip()
                else:
                    precio = "Precio no encontrado"

                # Eliminar el símbolo de la moneda
                precio_sin_simbolo = re.sub(r"[^\d.]", "", precio)

                # Convertir a float si es posible, de lo contrario dejar como está
                if precio_sin_simbolo:
                    precio_num = float(precio_sin_simbolo)
                    precio_num = math.ceil(precio_num)  # Redondear hacia arriba hasta el entero más cercano
                else:
                    precio_num = precio

                print(precio_num)

                # Calcular el precio de venta
                if 1 <= precio_num <= 9:
                    precio_venta = precio_num * 99
                elif 10 <= precio_num <= 14:
                    precio_venta = precio_num * 90
                elif 15 <= precio_num <= 17:
                    precio_venta = precio_num * 80
                elif 18 <= precio_num <= 20:
                    precio_venta = precio_num * 70          
                elif 21 <= precio_num <= 25:
                    precio_venta = precio_num * 64
                elif 26 <= precio_num <= 29:
                    precio_venta = precio_num * 60          
                elif 30 <= precio_num <= 35:
                    precio_venta = precio_num * 57
                elif 36 <= precio_num <= 39:
                    precio_venta = precio_num * 53        
                elif 40 <= precio_num <= 49:
                    precio_venta = precio_num * 50
                elif precio_num >= 50:
                    precio_venta = precio_num * 47
                else:
                    precio_venta = "No se pudo calcular el precio de venta"

                return {
                    "titulo": titulo, 
                    "precio": precio, 
                    "precio_venta": precio_venta, 
                    "imagenes": imagenes, 
                    "descripcion": descripcion
                }
                
        except requests.RequestException as e:
            print(f"Error: {e}")
        time.sleep(random.randint(3, 9))  
        pass
    

# Ingresa la URL de la página de Amazon
url = input("Por favor ingrese la URL de la página de Amazon: ")

# Obtén los ASINs de la página y conviértelos en un conjunto para eliminar los duplicados
asins_on_page = set(get_asins_from_page(url))
print(asins_on_page)

# Inicializa una lista para almacenar la información del producto
product_info_list = []


# Itera sobre cada ASIN
for asin in asins_on_page:
    # Genera la URL del producto
    product_url = f"https://www.amazon.com/-/es/dp/{asin}/"

    try:
        # Extrae la información del producto
        product_info = get_product_info(product_url)
        print(product_info)

        # Agrega la información del producto a la lista
        product_info_list.append(product_info)

    except Exception as e:
        print(f"Hubo un error al obtener la información del producto con ASIN {asin}: {e}")

    finally:
        # Espera un tiempo aleatorio entre 2 y 5 segundos
        time.sleep(random.uniform(2, 5))

# Define el nombre del archivo
filename = f"product_info_{datetime.now().strftime('%Y-%m-%d')}.csv"

import os

# Define el nombre del archivo con la ruta completa
filename = f"c:/amznfiles/product_info_{datetime.now().strftime('%Y-%m-%d')}.csv"

# Verifica si el archivo ya existe y cambia el nombre si es necesario
counter = 1
while os.path.exists(filename):
    filename = f"c:/amznfiles/product_info_{datetime.now().strftime('%Y-%m-%d')}_{counter}.csv"
    counter += 1

# Intenta abrir el archivo y escribir en él
try:
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)

        # Escribe los nombres de las columnas
        writer.writerow(product_info_list[0].keys())

        # Escribe los valores
        for product_info in product_info_list:
            writer.writerow(product_info.values())
except Exception as e:
    print(f"Hubo un error al guardar los datos en el archivo CSV: {e}")
else:
    if os.path.exists(filename):
        print(f"Los datos se han guardado con éxito en el archivo {filename}.")
    else:
        print("No se pudo crear el archivo.")

