import csv
import json
import re
import sys

import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
)

from saati_table import SaatiTable


class MyWindow(QtWidgets.QMainWindow):
    items = ['Краснодарский парень', 'Урбан', 'Нахлебник', 'Голый повар', 'Мясо под градусом']
    values = ['9', '7', '5', '3', '1', '1/3', '1/5', '1/7', '1/9']
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
        super(MyWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)

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

        table: QTableWidget = self.table
        expert_table: QTableWidget = self.expert_table
        choose_file: QPushButton = self.choose_file
        load_file: QPushButton = self.load_file
        save: QPushButton = self.save
        save_as: QPushButton = self.save_as
        expert_list: QListWidget = self.expert_list
        criterion_list: QListWidget = self.criterion_list

        for name, value in self.experts.items():
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, value)
            expert_list.addItem(item)
        expert_list.setCurrentRow(0)

        for name, value in self.criteria.items():
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, value)
            criterion_list.addItem(item)
        criterion_list.setCurrentRow(0)

        table.itemChanged.connect(self.item_changed)
        expert_table.itemChanged.connect(self.item_changed)
        expert_list.clicked.connect(self.update_view)
        criterion_list.clicked.connect(self.update_view)
        choose_file.clicked.connect(self.open_file_dialog)
        save.clicked.connect(self.update_data)
        save_as.clicked.connect(self.save_data_json)
        load_file.clicked.connect(self.load_data_json)

    @staticmethod
    def set_cell(table: QTableWidget, row, column, value):
        item = table.item(row, column)
        if item is None:
            item = QTableWidgetItem(value)
            table.setItem(row, column, item)
        else:
            item.setText(value)

    @staticmethod
    def get_cell(table: QTableWidget, row, column):
        item = table.item(row, column)
        if not item:
            item = QTableWidgetItem()
            table.setItem(row, column, item)
        return item.text()

    def is_view_valid(self, table: QTableWidget):
        size = table.rowCount()
        return all(
            SaatiTable.is_value_valid(self.get_cell(table, row, column))
            for row in range(size)
            for column in range(row + 1, size)
        )

    def update_data_from_view(self, data: SaatiTable, table: QTableWidget):
        if self.is_view_valid(table):
            for row in range(data.size()):
                for column in range(data.size()):
                    if row != column:
                        data.set_value(row, column, self.get_cell(table, row, column))
        else:
            for row in range(data.size()):
                for column in range(row + 1, data.size()):
                    if not SaatiTable.is_value_valid(self.get_cell(table, row, column)):
                        self.not_valid_item(table.item(row, column))

    def update_data(self):
        expert_list: QListWidget = self.expert_list
        criterion_list: QListWidget = self.criterion_list

        selected_expert = expert_list.currentItem().data(Qt.UserRole)
        selected_criterion = criterion_list.currentItem().data(Qt.UserRole)
        self.update_data_from_view(self.tables[selected_expert][selected_criterion], self.table)
        self.update_data_from_view(self.tables['experts'], self.expert_table)

    def update_view_from_data(self, data: SaatiTable, table: QTableWidget):
        for row in range(data.size()):
            for column in range(row + 1, data.size()):
                self.set_cell(table, row, column, data.get_value(row, column))

    def update_view(self):
        expert_list: QListWidget = self.expert_list
        criterion_list: QListWidget = self.criterion_list

        selected_expert = expert_list.currentItem().data(Qt.UserRole)
        selected_criterion = criterion_list.currentItem().data(Qt.UserRole)
        self.update_view_from_data(self.tables[selected_expert][selected_criterion], self.table)
        self.update_view_from_data(self.tables['experts'], self.expert_table)

    @staticmethod
    def not_valid_item(item: QTableWidgetItem):
        item.setBackground(QBrush(QColor(255, 0, 0)))

    def item_changed(self, item: QTableWidgetItem):
        row = item.row()
        column = item.column()
        if column <= row:
            return

        table: QTableWidget = item.tableWidget()
        value = self.get_cell(table, row, column)
        if value not in self.values:
            #  set red background
            self.not_valid_item(item)
            self.set_cell(table, column, row, '')
        else:
            item.setBackground(QBrush(QColor(255, 255, 255)))
            if value in ['3', '5', '7', '9']:
                self.set_cell(table, column, row, '1/{}'.format(value))
                return

            denominator = value if value == '1' else re.search(r'1/([3579])', value).group(1)
            self.set_cell(table, column, row, denominator)

    def open_file_dialog(self):
        file_path: QLineEdit = self.file_path

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", "", "*.json", options=options)
        if file_name:
            file_path.setText(file_name)

    def load_file_csv(self):
        file_path: QLineEdit = self.file_path

        with open(file_path.text()) as csv_file:
            data_reader = csv.reader(csv_file)
            for i in range(self.expert_count):
                self.experts[i] = np.matrix(data=[
                    data_reader.next() for _ in range(self.items_count)
                ])

    def csv_write_table(self, writer: csv.DictWriter, table, headers):
        writer.writerows(
            dict(zip(headers, row)) for row in table
        )

    def print_message(self, message: str, error: bool):
        messages: QPlainTextEdit = self.messages
        color = 'red' if error else 'green'
        messages.appendHtml("<p><font color=\"{}\">{}</font></p>".format(color, message))

    def save_data_to_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Open file", "", "*.csv", options=options)
        if file_name:
            with open(file_name, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, self.items)
                for expert in self.experts.values():
                    for criterion in self.criteria.values():
                        self.csv_write_table(writer, self.tables[expert][criterion], self.items)
                # self.csv_write_table(writer, self.tables['experts'], [1, 2, 3, 4])

    def load_data_json(self):
        file_path = self.file_path.text()
        if not file_path:
            self.print_message('Не указан путь к файлу', error=True)
            return

        with open(file_path) as file:
            data = json.load(file)

        self.tables = {}
        for expert in self.experts.values():
            self.tables[expert] = {}
            for criterion in self.criteria.values():
                self.tables[expert][criterion] = SaatiTable.from_data(self.items, data[expert][criterion])

        self.tables['experts'] = SaatiTable.from_data(self.experts, data['experts'])

        expert_list: QListWidget = self.expert_list
        criterion_list: QListWidget = self.criterion_list

        selected_expert = expert_list.currentItem().data(Qt.UserRole)
        selected_criterion = criterion_list.currentItem().data(Qt.UserRole)
        self.update_view_from_data(self.tables[selected_expert][selected_criterion], self.table)
        self.update_view_from_data(self.tables['experts'], self.expert_table)
        self.print_message('Данные загружены', error=False)

    def save_data_json(self):
        if not(
            all(
                self.tables[expert][criterion].is_valid()
                for expert in self.experts.values()
                for criterion in self.criteria.values()
            ) and self.tables['experts'].is_valid()
        ):
            self.print_message('Таблицы заполнены неправильно', error=True)
            return

        data = {}
        for expert in self.experts.values():
            data[expert] = {}
            for criterion in self.criteria.values():
                data[expert][criterion] = self.tables[expert][criterion].to_data()

        data['experts'] = self.tables['experts'].to_data()

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save file", "", "*.json", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                json.dump(data, file)

        self.print_message('Данные сохранены в файл {}'.format(file_name), error=False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
