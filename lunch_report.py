from collections import OrderedDict
from requests import get
import time
from pyperclip import copy

# user key: 
with open('../key.txt', 'rt') as f:
    user_key = f.read()
    
url_base = "https://developers.zomato.com/api/v2.1/"
header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": user_key}

ids = {"let's meat": 18494543,
  # "pizza u staré pece": 16512835 ,
  "olše": 16513849,
  "u vodoucha":  16506331,
  "sonora":  16506702,
  "incruenti": 18355481,
  # "u vodárny": 16506550,
  "hospůdka v ateliéru": 16506560,
  "nominanza": 16513818, 
  "vinohradský pivovar": 16507624}


def ask(query):
    res = get(url_base + query, headers=header)
    return res.json()


def menu(res_id):
    a = ask('dailymenu?res_id={}'.format(res_id))
    dishes = a['daily_menus'][0]['daily_menu']['dishes']
    dishes = [(dish['dish']['name'], dish['dish']['price']) for dish in dishes]
    # filter out empty price tags:
    dishes = [(name, price) for (name, price) in dishes if price]
    # uprav nazvy a ceny:
    dishes = [(name.strip(), price.split('\xa0')[0]) for (name, price) in dishes]
    return dishes


# jednotliva menu pujdou do slovniku:
data = dict()    
    
for (k,v) in ids.items():
    time.sleep(1)
    try:
        data[k] = menu(v)
    except Exception:
        pass


        
# restaurace, ktere nepokryva API:

import parsers as p

data['Infinity'] = p.Infinity(p.res_links['Infinity']).get_menu().name_price_pairs
# data['Prasatka'] = p.Prasatka(p.res_links['Prasatka']).get_menu().name_price_pairs 
# data['Fratello'] = p.Fratello(p.res_links['Fratello']).get_menu().name_price_pairs 
# data['Bila vrana'] = p.Vrana(p.res_links['Vrana']).get_menu().name_price_pairs 
data['Happy Bean'] = p.HappyBean(p.res_links['Happy Bean']).get_menu().name_price_pairs 
	
	
# setrid restaurace:
poradi = [# "incruenti",
          "Happy Bean", 
          "nominanza", 
          "let's meat",
          "Infinity", 
          # "Bila vrana", 
         # "Prasatka",
          "sonora",
          "olše", 
          "u vodoucha", 
          # "u vodárny", 
          "hospůdka v ateliéru", 
          "vinohradský pivovar"] 
          
data_ordered = OrderedDict()

for item in poradi:
    data_ordered[item] = data[item]
    
# vypis nekam data:
with open('lunch_report.txt', 'wt') as report:
    for (place, dishes) in data_ordered.items():
        report.write(place.upper())
        report.write('\n\n')
        for dish in dishes:
            try:
                report.write('\t'.join(dish))
                report.write('\n')
            except Exception:
                report.write('...\n')
        report.write('\n\n\n\n')
        
# vysledek do clipboardu:
with open('lunch_report.txt', 'rt') as report:
    copy(report.read())
    
