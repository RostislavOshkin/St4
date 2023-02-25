import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5 import uic


class OverW(QMainWindow):
    def __init__(self, id):
        global kost
        self.id = id
        super().__init__()
        uic.loadUi('overwrite.ui', self)
        res = "       "
        if kost.isdigit():
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            res = cur.execute(f"""Select * from main where id = {self.id}""").fetchone()
            con.close()
        kost = 'e'
        self.le_id.setText(str(res[0]))
        self.le_id.setReadOnly(True)
        self.le_names.setText(res[1])
        self.le_step.setText(str(res[2]))
        self.le_do.setText(res[3])
        self.le_des.setText(res[4])
        self.le_pri.setText(str(res[5]))
        self.le_vol.setText(str(res[6]))
        self.save.clicked.connect(self.save_)
        self.cancel.clicked.connect(self.cls)

    def cls(self):
        global kost
        kost = 's'
        self.close()

    def save_(self):
        global kost
        kost = 's'
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        if type(self.id) is str and len(self.id) > 1 and self.id[0] == 'w':
            self.id = self.id[1:]
        else:
            cur.execute(f"""Delete from main where id = {int(self.id)}""").fetchall()
            con.commit()
        res = f"""Insert into main VALUES ({int(self.id) + 1}, '{self.le_names.text()}', {self.le_step.text()}, '{self.le_do.text()}', '{self.le_des.text()}', {self.le_pri.text()}, {self.le_vol.text()})"""
        cur.execute(res)
        con.commit()
        con.close()
        self.close()


class Window(QMainWindow):
    def __init__(self):
        global kost
        kost = 'e'
        super().__init__()
        self.tableWidget = QTableWidget()
        self.max_id = 1
        uic.loadUi('main.ui', self)
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        res = cur.execute(f"""Select * from main""").fetchall()
        self.new_z.clicked.connect(self.write_)
        self.redact.clicked.connect(self.overwrite_)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID",
            "название сорта",
            "степень обжарки",
            "молотый/в зернах",
            "описание вкуса",
            "цена",
            "объем упаковки"])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(i + 1)
            for j in range(7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(res[i][j])))
                if int(res[i][0]) > self.max_id:
                    self.max_id = int(res[i][0])

    def overwrite_(self):
        global kost
        kost = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        self.close()

    def write_(self):
        global kost
        kost = 'w' + str(self.max_id)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    global kost
    kost = 's'
    while kost != 'e':
        if kost != 's':
            w = OverW(kost)
        else:
            w = Window()
        w.show()
        app.exec()
