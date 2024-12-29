import sqlite3
import sys

from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QApplication
from PyQt6.uic import loadUi


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeApp()
    ex.show()
    sys.exit(app.exec())
