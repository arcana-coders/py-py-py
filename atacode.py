from sp_api.api import Reports
from sp_api.base import Marketplaces, ReportType, ProcessingStatus
import time
import json
import csv


def load_keys(file_path):
    """
    Carga las claves de autenticación desde un archivo JSON.

    Args:
        file_path (str): Ruta al archivo JSON con las claves.

    Returns:
        dict: Diccionario con las claves de autenticación.
    """
    print("Intentando cargar claves desde:", file_path)
    try:
        with open(file_path, 'r') as file:
            keys = json.load(file)
        print("Claves cargadas correctamente.")
        return keys
    except FileNotFoundError:
        print(f"Archivo no encontrado: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error al parsear el archivo JSON: {e}")
    except Exception as e:
        print(f"Error inesperado al cargar claves: {e}")
    return None


# Define el marketplace
marketPlace = Marketplaces.MX

def getOrders():
    """
    Genera un reporte de órdenes, espera su procesamiento y guarda los datos en un archivo CSV.
    """
    print('Iniciando la obtención de órdenes...')
    
    # Define el tipo de reporte
    report_type = ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL
    print("Tipo de reporte seleccionado:", report_type)
    
    # Carga las credenciales
    credentials = load_keys('amzkeys.json')  # Ajusta la ruta
    if not credentials:
        print("No se pudieron cargar las credenciales. Deteniendo ejecución.")
        return
    
    print("Inicializando objeto Reports...")
    try:
        res = Reports(credentials=credentials, marketplace=marketPlace)
        print("Objeto Reports inicializado correctamente.")
    except Exception as e:
        print(f"Error al inicializar Reports: {e}")
        return
    
    # Crea el reporte
    try:
        print("Creando el reporte...")
        data = res.create_report(reportType=report_type, dataStartTime="2024-11-01T00:00:00Z")
        reportId = data.payload['reportId']
        print(f"Reporte creado. ID del reporte: {reportId}")
    except Exception as e:
        print(f"Error al crear el reporte: {e}")
        return
    
    # Espera hasta que el reporte esté procesado
    print("Esperando a que el reporte sea procesado...")
    while True:
        try:
            print("Consultando el estado del reporte...")
            report_status = res.get_report(reportId)
            status = report_status.payload.get('processingStatus')
            print(f"Estado actual del reporte: {status}")
            
            if status in [ProcessingStatus.DONE, ProcessingStatus.FATAL, ProcessingStatus.CANCELLED]:
                print("Reporte procesado o fallido. Saliendo del bucle.")
                break
            
            print("El reporte sigue procesándose. Esperando 2 segundos...")
            time.sleep(2)  # Espera 2 segundos antes de volver a comprobar
        except Exception as e:
            print(f"Error al verificar el estado del reporte: {e}")
            return
    
    # Verifica el resultado final
    if status == ProcessingStatus.DONE:
        print("Reporte completado exitosamente. Descargando los datos del reporte...")
        try:
            # Inspecciona el contenido completo de payload antes de continuar
            print("Contenido del payload de reporte:", report_status.payload)
            
            # Verifica si el reportDocumentId está presente
            report_document_id = report_status.payload.get('reportDocumentId')
            print(f"ID del documento del reporte: {report_document_id}")
            
            if not report_document_id:
                print("No se encontró 'reportDocumentId' en el payload.")
                return
            
            # Verifica si get_report_document existe en res
            if not hasattr(res, "get_report_document"):
                print("El objeto 'Reports' no tiene el método 'get_report_document'.")
                return
            
            # Descarga el contenido del reporte
            report_document = res.get_report_document(report_document_id)
            if not report_document:
                print("get_report_document devolvió None.")
                return
            
            print("Contenido del documento del reporte descargado:", report_document)
            content = report_document.decode('utf-8')  # Decodifica el contenido del reporte
            print("Reporte descargado exitosamente.")
            
            # Guarda el contenido en un archivo CSV
            with open('reporte_ordenes.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for line in content.splitlines():
                    writer.writerow(line.split('\t'))  # Supone que los datos están delimitados por tabulaciones
            print("Reporte guardado como 'reporte_ordenes.csv'.")
        except AttributeError as e:
            print(f"Error: parece que 'get_report_document' no es válido o no existe. {e}")
        except Exception as e:
            print(f"Error al descargar o guardar el reporte: {e}")
    else:
        print("El procesamiento del reporte falló o fue cancelado.")


# Punto de entrada
if __name__ == "__main__":
    print("Inicio del script...")
    print("Llamando a la función getOrders...")
    getOrders()
    print("Fin del script.")
