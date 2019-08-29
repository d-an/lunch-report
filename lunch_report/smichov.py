from lunch_report.parsing import Restaurant


class MeatCraft(Restaurant):
    def get_menu(self):
        foods = self.page.select('div.wpb_wrapper > h3 > b')
        self.name_price_pairs = [(food.text, '') for food in foods]
        return self


class UKristiana(Restaurant):
    def get_menu(self):
        menu = self.page.select('div.ukristiana-menu > div')
        hlavni = self.page.select('div.ukristiana-hlavnijidla > div')
        menu.extend(hlavni)
        self.name_price_pairs = [(item.text.strip(), '') for item in menu]
        return self


class Lavande(Restaurant):
    def get_menu(self):
        menu = self.page.find('div', class_='menus__menu-content')
