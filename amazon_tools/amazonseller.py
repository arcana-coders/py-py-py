import datetime
from mws import Orders

# Reemplaza con tus credenciales de acceso y detalles de la cuenta de Amazon MWS
access_key = 'Client ID'
secret_key = 'Client Secret'
account_id = 'Capalsa'
marketplace_id = 'A1AM78C64UM0Y8'

# Crea una instancia de la clase Orders
orders_api = Orders(access_key, secret_key, account_id, region='MX')

# Obtén los últimos 10 pedidos
now = datetime.datetime.utcnow()
response = orders_api.list_orders(marketplaceids=[marketplace_id], created_after=now-datetime.timedelta(days=30))

# Imprime los detalles de cada pedido
for order in response.orders:
    print('Pedido:', order.amazon_order_id)
    print('Fecha de creación:', order.purchase_date)
    print('Estado:', order.order_status)
    print('Total:', order.order_total.amount, order.order_total.currency)
    print('---')