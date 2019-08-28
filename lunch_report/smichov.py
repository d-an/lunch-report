from lunch_report.parsing import Restaurant


class MeatCraft(Restaurant):
    def get_menu(self):
        foods = self.page.select('div.wpb_wrapper > h3 > b')
        self.name_price_pairs = [(food.text, '') for food in foods]
        return self
