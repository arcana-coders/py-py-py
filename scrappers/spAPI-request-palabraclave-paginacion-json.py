import requests
import json
from datetime import datetime
import os
import time
from creds import credentials

# No olvides actualizar las credenciales en creds.py o donde decidas almacenarlas.
# credentials = {
#     "refresh_token": "tu_refresh_token",
#     "lwa_app_id": "tu_lwa_app_id",
#     "lwa_client_secret": "tu_lwa_client_secret",
# }

# Palabras clave para la búsqueda y la categoría específica
keywords = "weiman"
# category_id = "11525794011"

# Función para obtener el token de acceso LWA
def get_access_token():
    token_response = requests.post(
        "https://api.amazon.com/auth/o2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": credentials["refresh_token"],
            "client_id": credentials["lwa_app_id"],
            "client_secret": credentials["lwa_client_secret"],
        },
    )
    return token_response.json()["access_token"]

# Función para guardar la respuesta JSON
def save_to_json(data, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

# Función para realizar peticiones y manejar la paginación
def make_requests(access_token, next_token=None):
    endpoint = "https://sellingpartnerapi-na.amazon.com/catalog/2022-04-01/items"
    marketplace_id = "A1AM78C64UM0Y8"

    query_params = {
        "keywords": keywords,
        "marketplaceIds": marketplace_id,
        # "classificationId": category_id,
    }
    if next_token:
        query_params["pageToken"] = next_token

    headers = {
        "x-amz-access-token": access_token,
    }

    response = requests.get(endpoint, headers=headers, params=query_params)
    response_json = response.json()

    # Imprimir la respuesta
    print(json.dumps(response_json, indent=2))
    return response_json, response_json.get('pagination', {}).get('nextToken')

# Directorio para guardar los archivos
output_directory = "C:\\Users\\admin\\Desktop\\python-scrap-y-monitor\\txts"

# Obtener el access token inicial
access_token = get_access_token()

# Bucle para manejar múltiples páginas y guardar la respuesta en un archivo JSON
next_token = None
page_count = 1
while True:
    response_data, next_token = make_requests(access_token, next_token)
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{output_directory}\\{keywords}_{current_date}.json"
    
    # Guardar los datos en el archivo JSON
    save_to_json(response_data, filename)
    print(f"Datos de la página {page_count} guardados en {filename}")
    
    if not next_token:
        break  # No hay más páginas
    
    page_count += 1
    time.sleep(1)  # Esperar 1 segundo entre peticiones
