import requests

# Parámetros para la solicitud del token
LWA_URL = "https://api.amazon.com/auth/o2/token"
CLIENT_ID = "amzn1.application-oa2-client."
CLIENT_SECRET = "amzn1.oa2-cs.v1."
GRANT_TYPE = "client_credentials"  # Usar "client_credentials" para operaciones sin autorización del vendedor
REFRESH_TOKEN = "Atzr|-EKnrHjmB4Z--"  # Obtén esto cuando el vendedor autoriza tu aplicación
SCOPE = "sellingpartnerapi::notifications"

# Realizar solicitud para obtener el LWA access token
data = {
    "grant_type": GRANT_TYPE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": SCOPE
}

response = requests.post(LWA_URL, data=data)
token_info = response.json()

if "access_token" in token_info:
    access_token = token_info["access_token"]
else:
    print(f"Error obteniendo el access_token. Respuesta del servidor: {token_info}")
    exit()

# Una vez que tienes el token, puedes hacer llamadas a la API
API_ENDPOINT = "https://sellingpartnerapi-na.amazon.com/fba/inbound/v0/shipments/shipmentId1/preorder/confirm"
headers = {
    "host": "sellingpartnerapi-na.amazon.com",
    "user-agent": "Tu_Aplicacion/1.0 (Language=Python; Platform=tu_plataforma)",
    "x-amz-access-token": access_token,
    "x-amz-date": "fecha_actual"
}

response = requests.put(API_ENDPOINT, headers=headers)

# Imprimir respuesta
print(response.json())
