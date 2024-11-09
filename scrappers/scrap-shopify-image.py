import requests
import json
import pandas as pd


url = 'https://www.surginstruments.com/products.json?limit=250&page=1'

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
        print(len(imagen))
