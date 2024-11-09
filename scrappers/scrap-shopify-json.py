import requests
import json
import pandas as pd


url = 'https://www.surginstruments.com/products.json?limit=250&page=16'

r = requests.get(url)

data = r.json()

product_list = []

for item in data['products']:
    titulo = item['title']
    #descripcion = item['body_html']
    desc_corta = item['handle']
    proveedor = item['vendor']
    for imagen in item['images']:
        #print(imagen['src'])
        try:
            imagesrc = imagen['src']
        except:
            imagesrc = 'None'
    #print(imagen['src'])
    for variant in item['variants']:
        precio = variant['price']
        sku = variant['sku']
        disponible = variant['available']
    #print(precio,sku,disponible)
        product = {
            'titulo': titulo,
            'desc_corta': desc_corta,
            'proveedor': proveedor,
            'precio': precio,
            'sku': sku,
            'disponible': disponible,
            'imagen': imagesrc
        }
        product_list.append(product)


df = pd.DataFrame(product_list)
#print (df)
df.to_csv('surginstruments.csv')
print('saved to file.')



