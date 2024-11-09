import requests
from bs4 import BeautifulSoup

api_key = "c9c5725ddfa15759e306c456463f24b4"

# Solicitamos al usuario que proporcione la URL
url = input("Por favor, introduzca la URL del sitio web: ")
print("URL recibida, construyendo URL de la API...")

# Construimos la URL de la API
api_url = f"https://api.scraperapi.com?api_key={api_key}&url={url}"
print("URL de la API construida, realizando la solicitud...")

# Obtenemos el contenido de la página web a través de la API
response = requests.get(api_url)
print("Solicitud completada, analizando el contenido de la página...")

# Creamos un objeto BeautifulSoup con el contenido de la página web
soup = BeautifulSoup(response.text, 'html.parser')

# Buscamos el div con la clase especificada y obtenemos todos los links dentro de él
print("Buscando divs con la clase 'products product-cells clearfix'...")
product_divs = soup.find_all('div', {'class': 'products product-cells clearfix'})
for div in product_divs:
    print("Div encontrado, buscando enlaces dentro de él...")
    links = div.find_all('a', href=True)
    for link in links:
        print(f"Enlace encontrado: {link['href']}")
