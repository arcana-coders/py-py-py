#Este codigo extrae los ASIN de una pagina de producto, el producto es dado con el ASIN, y se va a otra
#pagina de producto random y descarga nuevamente los ASIN, y asi hasta completar 500. Entonces los guarda.

import csv
import random
import time

import requests
from bs4 import BeautifulSoup


def extract_asin_from_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    asins = set()
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and '/dp/' in href:
            asin = href.split('/dp/')[1].split('/')[0].split('?')[0]
            asins.add(asin)
    
    return asins

def main():
    asins = set()
    starting_asin = input('Enter an ASIN: ')
    asins.add(starting_asin)
    while len(asins) < 500:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Referer': 'https://www.google.com/'
        }
        random_product = random.choice(list(asins))
        response = requests.get(f'https://www.amazon.com/dp/{random_product}', headers=headers)
        asins_on_page = extract_asin_from_page(response.text)
        for asin in asins_on_page:
            if asin not in asins:
                asins.add(asin)
                print(asin)
        
        wait_time = random.uniform(3, 9)
        time.sleep(wait_time)
    
    now = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
    filename = f'ASIN {now}.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ASIN'])
        for asin in asins:
            writer.writerow([asin])


if __name__ == '__main__':
    main()
