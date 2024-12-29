import sqlite3
import sys

from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QApplication, QDialog, QMessageBox
from PyQt6.uic import loadUi


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)
        self.load_data()

        self.action_add.triggered.connect(self.add_coffee)
        self.action_edit.triggered.connect(self.edit_coffee)

    def load_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM coffee')
        res = cursor.fetchall()

        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах',
                                                    'Описание вкуса', 'Цена', 'Объем упаковки'])

        for i, row in enumerate(res):
            for j, item in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))

        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.resizeColumnToContents(i)

        conn.close()

    def add_coffee(self):
        form = AddEditCoffeeForm(self)
        if form.exec() == QDialog.accepted:
            self.load_data()

    def edit_coffee(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования.")
            return

        coffee_id = self.tableWidget.item(selected_row, 0).text()
        form = AddEditCoffeeForm(self, coffee_id)
        if form.exec() == QDialog.accepted:
            self.load_data()


class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__()
        loadUi('addEditCoffeeForm.ui', self)

        self.coffee_id = coffee_id
        self.parent = parent

        if self.coffee_id:
            self.actionButton.setText("Сохранить")
            self.actionButton.clicked.connect(self.update_coffee)
            self.load_coffee_data(self.coffee_id)
        else:
            self.actionButton.setText("Добавить")
            self.actionButton.clicked.connect(self.add_coffee)

    def load_coffee_data(self, coffee_id):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM coffee WHERE ID = {coffee_id}')
        row = cursor.fetchone()

        if row:
            self.nameEdit.setText(row[1])
            self.roastEdit.setText(row[2])
            self.groundEdit.setText(row[3])
            self.tasteEdit.setText(row[4])
            self.priceEdit.setText(str(row[5]))
            self.volumeEdit.setText(str(row[6]))

        conn.close()

    def add_coffee(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO coffee (name, roast_level, ground_beans, taste_description, price, volume)
            VALUES (?, ?, ?, ?, ?, ?)''', (
            self.nameEdit.text(),
            self.roastEdit.text(),
            self.groundEdit.text(),
            self.tasteEdit.text(),
            float(self.priceEdit.text()),
            float(self.volumeEdit.text())
        ))
        conn.commit()
        conn.close()
        self.accept()
        self.parent.load_data()

    def update_coffee(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE coffee
            SET name = ?, roast_level = ?, ground_beans = ?, taste_description = ?, price = ?, volume = ?
            WHERE id = ?''', (
            self.nameEdit.text(),
            self.roastEdit.text(),
            self.groundEdit.text(),
            self.tasteEdit.text(),
            float(self.priceEdit.text()),
            float(self.volumeEdit.text()),
            self.coffee_id
        ))
        conn.commit()
        conn.close()
        self.accept()
        self.parent.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeApp()
    ex.show()
    sys.exit(app.exec())
