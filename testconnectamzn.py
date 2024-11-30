import requests
import json
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from datetime import datetime

# Cargar configuración
with open('amzkeys.json', 'r') as config_file:
    config = json.load(config_file)

# Parámetros iniciales
region = 'us-east-1'
service = 'execute-api'
endpoint = 'https://sellingpartnerapi-na.amazon.com'

# Función para obtener el Access Token
def obtener_access_token():
    url = "https://api.amazon.com/auth/o2/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": config["lwa_client_id"],
        "client_secret": config["lwa_client_secret"],
        "refresh_token": config["lwa_token"]
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Error al obtener el Access Token: {response.status_code}, {response.text}")
        return None

# Función para obtener órdenes en un rango de fechas
def obtener_ordenes_en_rango():
    path = "/orders/v0/orders"
    url = f"{endpoint}{path}"

    # Obtener Access Token
    access_token = obtener_access_token()
    if not access_token:
        print("No se pudo obtener el Access Token.")
        return None, None

    # Parámetros de consulta
    params = {
        "MarketplaceIds": config["marketplace_id"],
        "CreatedAfter": "2024-11-01T00:00:00Z",  # Inicio del rango de búsqueda
        "OrderStatuses": "Pending,Unshipped,PartiallyShipped,Shipped",  # Buscar en todos los estados relevantes
        "MaxResultsPerPage": 100  # Máximo permitido por la API
    }

    # Crear solicitud AWSRequest
    request = AWSRequest(method="GET", url=url, params=params)
    request.headers['x-amz-access-token'] = access_token

    # Firmar la solicitud con SigV4Auth
    credentials = boto3.Session().get_credentials()
    SigV4Auth(credentials, service, region).add_auth(request)

    # Realizar la solicitud HTTP con requests
    response = requests.get(url, headers=dict(request.headers), params=params)
    return response.status_code, response.json()

# Ejecutar la consulta
status_code, response = obtener_ordenes_en_rango()

if status_code == 200:
    print("Estado:", status_code)
    print("Órdenes Encontradas:")
    print(json.dumps(response, indent=4))  # Formatear la respuesta con sangría

    # Manejo de paginación si hay más órdenes
    next_token = response.get('NextToken')
    while next_token:
        params["NextToken"] = next_token
        response = requests.get(url, headers=dict(request.headers), params=params).json()
        next_token = response.get('NextToken')
        print(json.dumps(response, indent=4))  # Imprimir datos adicionales
else:
    print(f"Estado: {status_code}")
    print("Error:", response)
