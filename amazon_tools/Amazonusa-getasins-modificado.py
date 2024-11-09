import csv
import random
import time
from bs4 import BeautifulSoup
import requests
import datetime

# Inicializar una lista vacía para almacenar los ASIN
ASIN_list = []

#Solicitar la URL a utilizar
amazonpage = input("Ingrese la página de Amazon que desea scrapear (incluir https://): ")

# Utilizar un ciclo while para recorrer las páginas de resultados de búsqueda
page = 1

while True:
    # Hacer una solicitud web a la página de resultados de búsqueda
    url = f"{amazonpage}{page}"
    print (url)
    headers = {
        "Referer": "https://www.google.com/",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    print (response)
    

    # Encontrar todos los elementos div que contienen los productos en la página
    products = soup.find_all('div', class_="zg-grid-general-faceout")
    # print (products)
    if not products:
        #raise Exception("No hay mas ASINS en esta busqueda.")
        break
    # Revisar cada producto
    for product in products:
        # Encontrar el elemento span que contiene el ASINS
        ASIN = product.find("div", {"class": "p13n-sc-uncoverable-faceout"})["id"]
        
            

        
        print(ASIN)

        # Añadir el ASIN a la lista si aun no está en ella
        if ASIN not in ASIN_list:
            ASIN_list.append(ASIN)
        

    # Verificar si hay más páginas
    if soup.find("li", class_="a-last"):
        page += 1
        
        # Elige un tiempo aleatorio para esperar antes de la siguiente petición
        time.sleep(random.randint(5,9))
    else:
        break
    
# Guarda los ASIN en un archivo CSV

now = datetime.datetime.now()
filename = f"ASIN-{now.strftime('%d%m%y')}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ASIN"])
    writer.writerows([[ASIN] for ASIN in ASIN_list])
    print("Archivo creado.")