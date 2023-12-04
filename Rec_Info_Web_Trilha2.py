import pip._vendor.requests as requests

url = 'https://www.petz.com.br/nossas-lojas'
res = requests.get(url)
html_page = res.text

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_page,'html.parser')

import re

stores =[]
for index, store in enumerate(soup.find_all("div", {"class": "store"}), start=1):
    name = store.find("h2", {"itemprop":"name"}).get_text().strip()
    address = store.find("p", {"itemprop": "address"})
    address = address.get_text()
    address = re.sub(' +', ' ',address)
    address = " ".join([s for s in address.strip().splitlines(False) if s.strip()])
    addressLoc = store.find("span", {"itemprop": "addressLocality"}).get_text().strip()
    telephone = store.find("p", {"itemprop": "telephone"}).get_text().strip()
    openingHours = store.find("p", {"itemprop": "openingHours"}).get_text().strip()
    region = store.find("span", {"itemprop": "addressRegion"}).get_text().strip()
    row = { 'name': name,                   'address': address,
            'telephone': telephone,         'openingHours':openingHours,
            'addressLocality': addressLoc,  'region': region}
    stores.append(row)

import csv
keys = stores[0].keys()
with open('stores.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(stores)