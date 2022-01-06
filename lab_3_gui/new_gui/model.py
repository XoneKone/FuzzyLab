import json

from saati_table import SaatiTable


class Model:
    items = ['Краснодарский парень', 'Урбан', 'Нахлебник', 'Голый повар', 'Мясо под градусом']
    experts = {
        'expert_1': 'Эксперт 1',
        'expert_2': 'Эксперт 2',
        'expert_3': 'Эксперт 3',
        'expert_4': 'Эксперт 4',
    }
    criteria = {
        'assortment': 'Разнообразие',
        'quantity': 'Качество',
        'delivery': 'Доставка',
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

    def is_valid(self):
        return all(
            (
                self.tables[expert][criterion].is_valid()
                for expert in self.experts
                for criterion in self.criteria
            )
        ) and self.tables['experts'].is_valid()

    def get_result(self):
        """
        Получает словарь, где ключами являются items, а значениями - значения функции принадлежности
        :return:
        """

        return {}

    # нормируем для таблиц экспертов Julia
    def norm_expert(self):
        list_average = self.tables['experts'].average()
        norm_list_expert = [(i / max(list_average)) for i in list_average]
        return norm_list_expert

    # нормируем для таблицы доверия Julia
    def norm_trust(self, expert, criterion):
        list_average = self.tables[expert][criterion].average()
        norm_list_trust = [(i / sum(list_average)) for i in list_average]
        return norm_list_trust

    def dump_json(self, path):
        if path:
            with open(path, 'w') as file:
                data = {'experts': self.tables['experts'].table}
                for expert in self.experts:
                    data[expert] = {}
                    for criterion in self.criteria:
                        data[expert][criterion] = self.tables[expert][criterion].table

                json.dump(data, file)

    def load_json(self, path):
        if path:
            with open(path) as file:
                data = json.load(file)
                self.tables['experts'] = SaatiTable.from_data(self.experts, data['experts'])
                for expert in self.experts:
                    self.tables[expert] = {}
                    for criterion in self.criteria:
                        self.tables[expert][criterion] = SaatiTable.from_data(self.items, data[expert][criterion])
