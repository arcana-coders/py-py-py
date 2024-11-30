import json
import time
from sp_api.api import Orders
from sp_api.base import Marketplaces, SellingApiException

def load_keys(file_path):
    """
    Carga las claves de autenticación desde un archivo JSON.

    Args:
        file_path (str): Ruta al archivo JSON con las claves.

    Returns:
        dict: Diccionario con las claves de autenticación.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def get_unsent_orders(keys_file):
    """
    Obtiene información de los pedidos no enviados del Marketplace.

    Args:
        keys_file (str): Ruta al archivo JSON con las claves.

    Returns:
        str: Información de los pedidos no enviados en formato JSON legible.
    """
    try:
        keys = load_keys(keys_file)
        
        orders_client = Orders(
            credentials=dict(
                refresh_token=keys['lwa_token'],
                lwa_app_id=keys['lwa_client_id'],
                lwa_client_secret=keys['lwa_client_secret']
            ),
            marketplace=Marketplaces.MX
        )

        all_orders = []
        next_token = None
        processing_status = "InProgress"  # Estado inicial ficticio para comenzar

        while processing_status not in ["Done", "Fail"]:
            print(f"Estado actual del procesamiento: {processing_status}. Esperando...")
            
            while True:
                # Realizar la solicitud inicial o con NextToken
                if next_token:
                    response = orders_client.get_orders(NextToken=next_token)
                else:
                    response = orders_client.get_orders(
                        CreatedAfter='2023-01-01T00:00:00Z',  # Fecha de filtro
                        OrderStatuses=['Pending', 'Unshipped', 'PartiallyShipped'],  # Estados no enviados
                    )
                
                # Agregar los pedidos obtenidos a la lista
                all_orders.extend(response.payload.get('Orders', []))
                
                # Verificar si hay más páginas
                next_token = response.payload.get('NextToken')
                if not next_token:
                    break  # Salir del bucle si no hay más páginas
                
                # Pausa para evitar superar los límites de tasa de solicitudes
                time.sleep(2)
            
            # Comprobar el estado del procesamiento
            processing_status = response.payload.get("ProcessingStatus", "Done")
            
            if processing_status not in ["Done", "Fail"]:
                time.sleep(5)  # Pausar antes de verificar el estado nuevamente

        # Convertir la lista de pedidos a JSON legible
        readable_json = json.dumps(all_orders, indent=4, ensure_ascii=False)
        return readable_json

    except SellingApiException as e:
        return f"Error en la API de Amazon: {e}"
    except Exception as e:
        return f"Error general: {e}"

if __name__ == '__main__':
    keys_file_path = 'amzkeys.json'
    unsent_orders = get_unsent_orders(keys_file_path)
    print(unsent_orders)
