import requests
import json

# Tus credenciales de la API de Amazon
CLIENT_ID = 'amzn1.application-oa2-client'
CLIENT_SECRET = 'amzn1.oa2-cs.v1.'
REFRESH_TOKEN = 'Atzr|'

# Endpoint para obtener el access token
ENDPOINT_TOKEN = 'https://api.amazon.com/auth/o2/token'

# Headers y data para la petición de access token
headers = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
}
data = {
    'grant_type': 'refresh_token',
    'refresh_token': REFRESH_TOKEN,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
}

response = requests.post(ENDPOINT_TOKEN, headers=headers, data=data)
response_json = response.json()

# Si todo va bien, deberías obtener un access_token
ACCESS_TOKEN = response_json.get('access_token')

# Imprimir respuesta completa en caso de error
if not ACCESS_TOKEN:
    print(f"Respuesta de error: {response_json}")

print(f"Access Token obtenido: {ACCESS_TOKEN}")

