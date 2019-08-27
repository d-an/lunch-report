import lunch_report.flora as p
from collections import OrderedDict
from requests import get
import time
import os
from jinja2 import Template


# user key:
user_key = os.environ['user_key']

url_base = "https://developers.zomato.com/api/v2.1/"
header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": user_key}


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

for (name, id) in p.ids.items():
    time.sleep(1)
    try:
        if name == 'prasatka':
            data[name] = menu(id, remove_empty_prices=False)
        else:
            data[name] = menu(id, remove_empty_prices=True)
    except Exception:
        broken.append(name)


# restaurants not available through zomato:

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

with open('lunch_report/lunch_report.template', 'rt') as f:
    template = Template(f.read())

with open('lunch_report/lunch_report.html', 'wt') as f:
    f.write(template.render(data_ordered=data_ordered))
