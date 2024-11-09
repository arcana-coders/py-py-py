import requests
import random
from bs4 import BeautifulSoup
import time
import pandas as pd
import datetime
from termcolor import colored

# Leer el archivo CSV de ASINs
df = pd.read_csv("ASIN 2023-02-15 18-10-41.csv")

# Lista para guardar los ASIN que cumplen con la última opción
result = []

# Variable para almacenar la última página de Amazon visitada
last_page = "https://www.amazon.com.mx/"

for index, row in df.iterrows():
    asin = row["ASIN"]
    if pd.isnull(asin):
        continue
    asin = str(asin)
    url = f"https://www.amazon.com.mx/gp/product/" + asin + "/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Referer": last_page
    }
    
    print(f"Usando referer {headers['Referer']}")
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    availability = soup.find(id="availability")

    if availability is None:
        print(f"El producto con ASIN {asin} no está publicado")
    elif "Disponible" in availability.text:
        print(f"El producto con ASIN {asin} ya tiene vendedor")
    elif "No disponible por el momento" in availability.text:
        print(colored(f"Eureka!! El producto con ASIN {asin} lo guardamos", "red"))
        result.append(asin)

    # Establecer la última página visitada en Amazon como el referer para la próxima solicitud
    last_page = url
    
    # Generar un tiempo de retraso aleatorio entre 3 y 8 segundos
    delay = random.uniform(3, 12)
    time.sleep(delay)

# Escribir los ASIN resultantes en un archivo CSV nuevo
now = datetime.datetime.now()
result_df = pd.DataFrame({"ASIN": result})
filename = now.strftime("result_%Y-%m-%d_%H-%M-%S.csv")
result_df.to_csv(filename, index=False)


