# -*- coding: utf-8 -*-

from requests import get
from bs4 import BeautifulSoup


class Restaurant:
    def __init__(self, link):
        self.page = BeautifulSoup(get(link).content.decode('utf-8'))

    def get_menu(self):
        pass


# a class useful for Fratello:           
class Foods:
    def __init__(self):
        self.foods = []

    def add_day(self):
        self.foods.append([])

    def add_food(self, food):
        if self.foods:
            self.foods[-1].append(food)
