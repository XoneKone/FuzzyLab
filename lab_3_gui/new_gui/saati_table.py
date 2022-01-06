# Model
import json

import numpy as np


class SaatiTable:
    values = ['9', '7', '5', '3', '1', '1/3', '1/5', '1/7', '1/9']

    def __init__(self, items):
        self.items = items
        size = len(items)
        self.table = [
            ['1' if row == column else '' for row in range(size)] for column in range(size)
        ]

    def is_valid(self):
        return all(
            self.is_value_valid(value)
            for row in self.table
            for value in row
        )

    @staticmethod
    def is_value_valid(value):
        return value in SaatiTable.values

    def get_value(self, row, column):
        return self.table[row][column]

    def set_value(self, row, column, value):
        if self.is_value_valid(value):
            self.table[row][column] = value
            if value in ('3', '5', '7', '9'):
                self.table[column][row] = '1/{}'.format(value)
            else:
                self.table[column][row] = value[-1]

    def size(self):
        return len(self.items)

    @staticmethod
    def from_data(items, data: list[list[str]]):
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

    def value_to_float(self, value: str):
        if not self.is_value_valid(value):
            return None

        try:
            return float(value)
        except ValueError:
            return 1 / float(value[-1])

    def to_numpy(self):
        if not self.is_valid():
            return

        return np.matrix(
            data=[[self.value_to_float(value) for value in row] for row in self.table]
        )

    # Julia
    def average(self):
        pr = 1
        list_average = []
        size = len(self.items)
        for i in range(size):
            for j in range(size):
                pr *= self.table[i][j]
            list_average.append(pr ** (1 / size))
        return list_average

