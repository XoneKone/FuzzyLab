from typing import List


class SaatiTable:
    values = ['9', '7', '5', '3', '1', '1/3', '1/5', '1/7', '1/9']

    def __init__(self, items):
        self.items = items
        size = len(items)
        self.table = [
            ['1' if row == column else '' for row in range(size)] for column in range(size)
        ]

    def is_cell_valid(self, row, column):
        return self.table[row][column] in self.values

    @staticmethod
    def is_value_valid(value):
        return value in SaatiTable.values

    def is_valid(self):
        return all(
            self.is_cell_valid(row, column)
            for row in range(len(self.table))
            for column in range(len(self.table))
        )

    def get_value(self, row, column):
        return self.table[row][column]

    def set_value(self, row, column, value):
        self.table[row][column] = value

    def size(self):
        return len(self.items)

    @staticmethod
    def from_data(items, data: List[List[str]]):
        table = SaatiTable(items)
        for row in range(table.size()):
            for column in range(table.size()):
                if row != column:
                    table.set_value(row, column, data[row][column])
        return table

    def to_data(self):
        return [
            [
                self.get_value(row, column)
                for row in range(len(self.table))
            ]
            for column in range(len(self.table))
        ]