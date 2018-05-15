# -*- coding: utf-8 -*-

from requests import get
from bs4 import BeautifulSoup
from datetime import datetime

res_links = {'Infinity': 'http://www.infinitybar.cz/restaurace/poledni-menu',
             'Prasatka': 'http://www.triprasatka.cz/home-page/lunch/',
             'Fratello': 'http://www.ristorantefratello.cz/poledni-menu/',
             'Vrana': 'http://www.bilavrana.com/cs/poledni-menu',
             'Happy Bean': 'http://www.happybean.cz/denni-menu/',
             'Roma Uno': 'https://romauno.cz/cs/obedove-menu'}


class Restaurant:
    def __init__(self, link):
        self.page = BeautifulSoup(get(link).content.decode('utf-8'), "lxml")

    def get_menu(self):
        pass


class Infinity(Restaurant):
    def process_pair(self, pair):
        if len(pair) == 2:
            return pair[0].strip(), pair[1].split(']')[-1].strip()
        else:
            return pair[0].replace('\n', '').strip(), ''

    def get_menu(self):
        day_num = datetime.now().weekday() + 1
        tables = self.page.find_all('table')
        whole_week = tables[2]
        todays_menu = tables[2 + day_num]
        rows = whole_week.find_all('tr')
        rows.extend(todays_menu.find_all('tr'))
        name_price_pairs = [item.text.split('\t') for item in rows]
        self.name_price_pairs = [self.process_pair(pair) for pair in name_price_pairs]
        return self


class Prasatka(Restaurant):
    def get_menu(self):
        hlavni_jidla = self.page.find_all('ul', class_='menu-list__items')[2]
        names = [item.find(class_='item_title').contents[0] for item in hlavni_jidla.find_all('li')]
        prices = [item.find(class_='menu-list__item-price').contents[0] for item in hlavni_jidla.find_all('li')]
        if len(names) != len(prices):
            prices = ['' for item in names]
        self.name_price_pairs = list(zip(names, prices))
        return self


# a class useful for Fratello:           
class Foods:
    def __init__(self):
        self.foods = []

    def add_day(self):
        self.foods.append([])

    def add_food(self, food):
        if self.foods:
            self.foods[-1].append(food)


class Fratello(Restaurant):
    def name_price(row):
        items = row.split('…')
        if len(items) == 1:
            items = [items[0], '']
        return items

    def get_menu(self):
        ps = self.page.find_all('p')
        ps = [item.text.strip() for item in ps]
        ps = [item for item in ps if item]
        ps2 = [item.split(' ')[0] for item in ps]
        foods = Foods()
        days = ['PONDĚLÍ', 'ÚTERÝ', 'STŘEDA', 'ČTVRTEK', 'PÁTEK']
        for num, word in enumerate(ps2):
            if word in days:
                foods.add_day()
            else:
                foods.add_food(ps[num])
        weeks_menus = dict(zip(days, foods.foods))
        weekday = datetime.now().weekday()
        todays_menu = weeks_menus[days[weekday]]
        self.name_price_pairs = [Fratello.name_price(item) for item in todays_menu]
        return self


class Vrana(Restaurant):
    def get_menu(self):
        menus = self.page.find_all('table', class_="jidelak_normal napojak denni")
        dates = [menu.find('tr') for menu in menus]
        weekday = datetime.now().weekday()
        weekday = ['Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek'][weekday]
        menu = [menu for day, menu in zip(dates, menus) if weekday in day.text][0]
        foods = menu.find_all('tr')[2:]
        self.name_price_pairs = [[item.text for item in food.find_all('td')] for food in foods]
        return self


class HappyBean(Restaurant):
    def get_menu(self):
        spans = self.page.find_all('span')
        # the number of the span where daily menus start:
        start = [span for span in enumerate(spans) if 'DENNÍ MENU' in span[1].text][-1][0]
        spans_filtered = spans[start:]
        spans_filtered = [item.text for item in spans_filtered if item.text]
        # this is what i'll use to separate menus for individual days:
        days = ['PONDĚLÍ', 'ÚTERÝ', 'STŘEDA', 'ČTVRTEK', 'PÁTEK', 'KDY MÁME OTEVŘENO']
        delimiters = iter(days)
        delimiter = next(delimiters)
        menus = Foods()
        lines = iter(spans_filtered)
        while True:
            try:
                line = next(lines)
                if delimiter in line:
                    menus.add_day()
                    delimiter = next(delimiters)
                else:
                    menus.add_food(line)
            except StopIteration:
                break
        weeks_menus = dict(zip(days[:-1], menus.foods[:-1]))
        weekday = datetime.now().weekday()
        todays_menu = weeks_menus[days[weekday]]
        # for some reason there can be duplicities:
        todays_menu = list(set(todays_menu))
        self.name_price_pairs = [(food, '') for food in todays_menu]
        return self


class RomaUno(Restaurant):
    def get_menu(self):
        # now = str(datetime.now().weekday() + 1)
        # menu = self.page.find_all('div', attrs={'class': 'daily-slide', 'data-slide': now})[0]
        menu = self.page.find_all('div', class_='daily-slide today')[0]
        names = menu.find_all('div', class_='food-name')
        names = [name.contents[0] for name in names]
        prices = menu.find_all('div', class_='food-price')
        prices = [price.contents[0] for price in prices]
        self.name_price_pairs = list(zip(names, prices))
        return self
