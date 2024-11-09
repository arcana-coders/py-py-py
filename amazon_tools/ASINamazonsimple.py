import csv
import random
import time
from bs4 import BeautifulSoup
import requests

# Inicializar una lista vacía para almacenar los ASINs que no tienen un precio
ASIN_list = []

# Leer el archivo CSV con la lista de ASINs
with open("ASIN.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Saltar la primera línea (encabezados)
    for row in reader:
        ASIN = row[0]
        # Crear la URL con el ASIN actual
        url = f"https://www.amazon.com.mx/dp/{ASIN}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0'}
        response = requests.get(url, headers=headers)
        print(response)
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar el elemento con la clase "a-price-decimal"
        price_element = soup.find("span", {"class": "a-price-whole"})
        if price_element is None:
            print (ASIN)
            print ("Este producto nadie lo esta vendiendo. FELICIDADES!!")
        # Si no se encuentra el elemento, guardar el ASIN en la lista y escribirlo en el archivo CSV
        if price_element is None:
            ASIN_list.append(ASIN)
            with open("ASINSparasubir.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ASIN"])
                writer.writerows([[ASIN] for ASIN in ASIN_list])

        # Esperar entre 6 y 10 segundos antes de la siguiente prueba
        time.sleep(random.randint(6,10))
