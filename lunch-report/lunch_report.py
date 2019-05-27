from collections import OrderedDict
from requests import get
import time
import os

# user key:
user_key = os.environ['user_key']

url_base = "https://developers.zomato.com/api/v2.1/"
header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": user_key}

ids = {"let's meat": 18494543,
       "olše": 16513849,
       "u vodoucha": 16506331,
       "sonora": 16506702,
       "incruenti": 18355481,
       "u vodárny": 16506550,
       "hospůdka v ateliéru": 16506560,
       "nominanza": 16513818,
       "vinohradský pivovar": 16507624,
       "prasatka": 18325358}


def ask(query):
    res = get(url_base + query, headers=header)
    return res.json()


def menu(res_id, remove_empty_prices=True):
    a = ask('dailymenu?res_id={}'.format(res_id))
    dishes = a['daily_menus'][0]['daily_menu']['dishes']
    dishes = [(dish['dish']['name'], dish['dish']['price']) for dish in dishes]
    # filter out empty price tags:
    if remove_empty_prices:
        dishes = [(name, price) for (name, price) in dishes if price]
    # modify names and prices:
    dishes = [(name.strip(), price.split('\xa0')[0]) for (name, price) in dishes]
    return dishes


# menus will go into this dictionary:
data = dict()

broken = []

for (name, id) in ids.items():
    time.sleep(1)
    try:
        if name == 'prasatka':
            data[name] = menu(id, remove_empty_prices=False)
        else:
            data[name] = menu(id, remove_empty_prices=True)
    except Exception:
        broken.append(name)


# restaurants not available through zomato:
import parsers as p

others = {'Infinity': p.Infinity,
          # 'Prasatka': p.Prasatka,
          'Fratello': p.Fratello,
          'Bila vrana': p.Vrana,
          'Happy Bean': p.HappyBean,
          'Roma Uno': p.RomaUno,
          'La Farma': p.LaFarma
          }


for name, parser in others.items():
    try:
        data[name] = parser(p.res_links[name]).get_menu().name_price_pairs
    except Exception:
        broken.append(name)

# sort the restaurants:
poradi = ["incruenti",
          "Happy Bean",
          "La Farma",
          "nominanza",
          "Fratello",
          "let's meat",
          "Infinity",
          "Roma Uno",
          "Bila vrana",
          "prasatka",
          "sonora",
          "olše",
          "u vodoucha",
          "u vodárny",
          "hospůdka v ateliéru",
          "vinohradský pivovar"]

# include only those that we got in data:
poradi = [item for item in poradi if item in data]

# choose the order:
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
                report.write(' '.join(dish))
                report.write('\n')
            except Exception:
                report.write('...\n')
        report.write('\n\n\n\n')
    for item in broken:
        report.write(item + '\n')

