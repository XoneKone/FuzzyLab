import sys

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
    QPlainTextEdit, QMessageBox,
)

from model import Model


class MyWindow(QtWidgets.QMainWindow):
    NOT_VALID_DATA_MESSAGE = 'Некорректные значения в таблице'
    DATA_SAVED_MESSAGE = 'Данные успешно сохранены'
    DATA_LOADED_MESSAGE = 'Данные успешно загружены'
    FILE_NOT_EXIST_MESSAGE = 'Файл не существует'

    def __init__(self, model: Model):
        super(MyWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.model = model

        table: QTableWidget = self.table
        expert_table: QTableWidget = self.expert_table
        choose_file: QPushButton = self.choose_file
        load_file: QPushButton = self.load_file
        save: QPushButton = self.save
        save_as: QPushButton = self.save_as
        calculate: QPushButton = self.calculate
        expert_list: QListWidget = self.expert_list
        criterion_list: QListWidget = self.criterion_list

        for value, name in model.experts.items():
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, value)
            expert_list.addItem(item)
        expert_list.setCurrentRow(0)

        for value, name in model.criteria.items():
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, value)
            criterion_list.addItem(item)
        criterion_list.setCurrentRow(0)

        table.itemChanged.connect(self.item_changed)
        expert_table.itemChanged.connect(self.item_changed)
        expert_list.clicked.connect(self.update_view)
        criterion_list.clicked.connect(self.update_view)
        choose_file.clicked.connect(self.open_file_dialog)
        save.clicked.connect(self.update_model)
        save_as.clicked.connect(self.dump_json)
        load_file.clicked.connect(self.load_json)
        calculate.clicked.connect(self.get_result)

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

    def is_table_valid(self, table: QTableWidget):
        size = table.rowCount()
        return all(
            Model.is_value_valid(self.get_cell(table, row, column))
            for row in range(size)
            for column in range(size)
            if row != column
        )

    def highlight_table(self, table: QTableWidget):
        size = table.rowCount()
        for row in range(size):
            for column in range(row + 1, size):
                if not Model.is_value_valid(self.get_cell(table, row, column)):
                    self.highlight_cell(table.item(row, column))

    def update_model(self):
        expert_list: QListWidget = self.expert_list
        criterion_list: QListWidget = self.criterion_list

        selected_expert = expert_list.currentItem().data(Qt.UserRole)
        selected_criterion = criterion_list.currentItem().data(Qt.UserRole)

        item_table: QTableWidget = self.table
        expert_table: QTableWidget = self.expert_table

        if self.is_table_valid(item_table) and self.is_table_valid(expert_table):
            expert_size = len(self.model.experts)
            for row in range(expert_size):
                for column in range(expert_size):
                    if row != column:
                        self.model.set_value_expert(row, column, self.get_cell(expert_table, row, column))

            item_size = len(self.model.items)
            for row in range(item_size):
                for column in range(item_size):
                    if row != column:
                        self.model.set_value_item(
                            selected_expert, selected_criterion, row, column, self.get_cell(item_table, row, column)
                        )

            self.print_message(self.DATA_SAVED_MESSAGE)
        else:
            self.highlight_table(item_table)
            self.highlight_table(expert_table)
            self.print_message(self.NOT_VALID_DATA_MESSAGE, error=True)

    def update_view(self):
        expert_list: QListWidget = self.expert_list
        criterion_list: QListWidget = self.criterion_list

        selected_expert = expert_list.currentItem().data(Qt.UserRole)
        selected_criterion = criterion_list.currentItem().data(Qt.UserRole)

        item_table: QTableWidget = self.table
        expert_table: QTableWidget = self.expert_table

        expert_size = len(self.model.experts)
        for row in range(expert_size):
            for column in range(expert_size):
                if row != column:
                    self.set_cell(expert_table, row, column, self.model.get_value_expert(row, column))

        item_size = len(self.model.items)
        for row in range(item_size):
            for column in range(item_size):
                if row != column:
                    self.set_cell(
                        item_table,
                        row,
                        column,
                        self.model.get_value_item(selected_expert, selected_criterion, row, column),
                    )

    @staticmethod
    def highlight_cell(item: QTableWidgetItem):
        item.setBackground(QBrush(QColor(255, 0, 0)))

    def item_changed(self, item: QTableWidgetItem):
        table: QTableWidget = item.tableWidget()
        item_table: QTableWidget = self.table

        row = item.row()
        column = item.column()
        if column <= row:
            return

        value = self.get_cell(table, row, column)
        if self.model.is_value_valid(value):
            item.setBackground(QBrush(QColor(50, 50, 50)))
            if table is item_table:
                expert_list: QListWidget = self.expert_list
                criterion_list: QListWidget = self.criterion_list

                selected_expert = expert_list.currentItem().data(Qt.UserRole)
                selected_criterion = criterion_list.currentItem().data(Qt.UserRole)
                self.model.set_value_item(selected_expert, selected_criterion, row, column, value)
                opposite_value = self.model.get_value_item(selected_expert, selected_criterion, column, row)
            else:
                self.model.set_value_expert(row, column, value)
                opposite_value = self.model.get_value_expert(column, row)

            self.set_cell(table, column, row, opposite_value)
        else:
            self.highlight_cell(item)
            self.set_cell(table, column, row, '')

    def open_file_dialog(self):
        file_path: QLineEdit = self.file_path

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", "", "*.json", options=options)
        if file_name:
            file_path.setText(file_name)

    def print_message(self, message: str, error: bool = False):
        messages: QPlainTextEdit = self.messages
        color = 'red' if error else 'green'
        messages.appendHtml("<p><font color=\"{}\">{}</font></p>".format(color, message))

    def dump_json(self):
        path = self.file_path.text()
        if path:
            if self.model.is_valid():
                self.model.dump_json(path)
                self.print_message(self.DATA_SAVED_MESSAGE)
            else:
                self.print_message(self.NOT_VALID_DATA_MESSAGE, error=True)
        else:
            self.print_message(self.FILE_NOT_EXIST_MESSAGE, error=True)

    def load_json(self):
        path = self.file_path.text()
        if path:
            self.model.load_json(path)
            self.update_view()
            self.print_message(self.DATA_LOADED_MESSAGE)
        else:
            self.print_message(self.FILE_NOT_EXIST_MESSAGE, error=True)

    def get_result(self):
        if self.model.is_valid():
            #result = self.model.get_result()
            result = {'jdlf dflj ': 0.123, 'eurueworeu': 0.364883}
            text = []
            for name, value in result.items():
                text.append('{}: {}\n'.format(name, value))
            msg = QMessageBox(QMessageBox.Information, 'Оценки', ''.join(text))
            msg.exec()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(Model())
    window.show()
    sys.exit(app.exec_())
