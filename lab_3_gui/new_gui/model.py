import json

from saati_table import SaatiTable


class Model:
    items = ['Краснодарский парень', 'Урбан', 'Нахлебник', 'Голый повар', 'Мясо под градусом']
    experts = {
        'Эксперт 1': 'expert_1',
        'Эксперт 2': 'expert_2',
        'Эксперт 3': 'expert_3',
        'Эксперт 4': 'expert_4',
    }
    criteria = {
        'Разнообразие': 'assortment',
        'Качество': 'quantity',
        'Доставка': 'delivery',
    }

    def __init__(self):
        self.tables = {
            'experts': SaatiTable(self.experts.values()),
            'expert_1': {
                'assortment': SaatiTable(self.items),
                'quantity': SaatiTable(self.items),
                'delivery': SaatiTable(self.items),
            },
            'expert_2': {
                'assortment': SaatiTable(self.items),
                'quantity': SaatiTable(self.items),
                'delivery': SaatiTable(self.items),
            },
            'expert_3': {
                'assortment': SaatiTable(self.items),
                'quantity': SaatiTable(self.items),
                'delivery': SaatiTable(self.items),
            },
            'expert_4': {
                'assortment': SaatiTable(self.items),
                'quantity': SaatiTable(self.items),
                'delivery': SaatiTable(self.items),
            },
        }

    def set_value_expert(self, row, column, value):
        self.tables['experts'].set_value(row, column, value)

    def get_value_expert(self, row, column):
        return self.tables['experts'].get_value(row, column)

    def set_value_item(self, expert, criterion, row, column, value):
        self.tables[expert][criterion].set_value(row, column, value)

    def get_value_item(self, expert, criterion, row, column):
        return self.tables[expert][criterion].get_value(row, column)

    @staticmethod
    def is_value_valid(value):
        return SaatiTable.is_value_valid(value)

    def get_result(self):
        """
        Получает словарь, где ключами являются items, а значениями - значения функции принадлежности
        :return:
        """

        return {}

    def save_json(self, path):
        if path:
            with open(path, 'w') as file:
                json.dump(data, file)

