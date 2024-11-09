import requests
import datetime
import json
from creds import credentials

# Tu ASIN objetivo
asin = "B01N6ZPQWW"  # Reemplaza esto con el ASIN real del producto que quieres revisar
marketplace_ids = "A1AM78C64UM0Y8"  # Reemplaza esto con el ID del marketplace correspondiente

# Obteniendo el token de acceso LWA
token_response = requests.post(
    "https://api.amazon.com/auth/o2/token",
    data={
        "grant_type": "refresh_token",
        "refresh_token": credentials["refresh_token"],
        "client_id": credentials["lwa_app_id"],
        "client_secret": credentials["lwa_client_secret"],
    },
)
access_token = token_response.json()["access_token"]

# Endpoint de la SP API para América del Norte con la versión de fecha de la API
endpoint = "https://sellingpartnerapi-na.amazon.com/catalog/2022-04-01/items/{}".format(asin)

# Parámetros para la consulta de la API
query_params = {
    "marketplaceIds": marketplace_ids,
    "includedData": "summaries",  # Puedes agregar más conjuntos de datos aquí si es necesario
    # "locale": "en_US"  # Descomenta y reemplaza si necesitas especificar un local distinto
}

# Realizar la petición GET para obtener información del producto
headers = {
    "x-amz-access-token": access_token,
}

response = requests.get(
    endpoint,
    headers=headers,
    params=query_params  # Pasar los parámetros de consulta con la solicitud
)

# Imprimir la respuesta JSON de manera legible
print(json.dumps(response.json(), indent=2))

