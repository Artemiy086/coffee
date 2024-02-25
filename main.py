import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import QtWidgets, QtCore


class Ui_Add(object):
    def setupUi(self, Add):
        Add.setObjectName("Add")
        Add.resize(450, 350)
        self.centralwidget = QtWidgets.QWidget(Add)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.title = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.title.setObjectName("title")
        self.gridLayout.addWidget(self.title, 0, 1, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)

        self.stepen = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.stepen.setObjectName("stepen")
        self.gridLayout.addWidget(self.stepen, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.zerno = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.zerno.setObjectName("zerna")
        self.gridLayout.addWidget(self.zerno, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.desc = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.desc.setObjectName("desc")
        self.gridLayout.addWidget(self.desc, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.v = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.v.setObjectName("title")
        self.gridLayout.addWidget(self.v, 4, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.price = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.price.setObjectName("price")
        self.gridLayout.addWidget(self.price, 5, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 6, 1, 1, 1)
        Add.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Add)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 26))
        self.menubar.setObjectName("menubar")
        Add.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Add)
        self.statusbar.setObjectName("statusbar")
        Add.setStatusBar(self.statusbar)

        self.retranslateUi(Add)
        QtCore.QMetaObject.connectSlotsByName(Add)

    def retranslateUi(self, Add):
        _translate = QtCore.QCoreApplication.translate
        Add.setWindowTitle(_translate("Add", "MainWindow"))
        self.label_1.setText(_translate("Add", "название сорта"))
        self.label_2.setText(_translate("Add", "степень обжарки"))
        self.label_3.setText(_translate("Add", "молотый/в зернах"))
        self.label_4.setText(_translate("Add", "описание вкуса"))
        self.label_5.setText(_translate("Add", "объем упаковки"))
        self.label_6.setText(_translate("Add", "цена"))

        self.pushButton.setText(_translate("Add", "Добавить"))


class AddWidget(QMainWindow, Ui_Add):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.con = sqlite3.connect("coffees.sqlite")
        self.pushButton.clicked.connect(self.add_elem)
        self.add_status = False

    def add_elem(self):
        cur = self.con.cursor()
        try:
            title = self.title.toPlainText()
            desc = self.desc.toPlainText()
            price = self.price.toPlainText()
            zerno = self.zerno.toPlainText()
            stepen = self.stepen.toPlainText()
            V = float(self.v.toPlainText())

            if len(title) == 0 or len(desc) == 0 or\
                    len(zerno) == 0 or len(stepen) == 0 or len(price) == 0:
                raise Exception()

            cur.execute("INSERT INTO coffee VALUES (?,?,?,?,?,?,?)",
                        (cur.execute("SELECT max(id) FROM coffees").fetchone()[0] + 1,
                         title, stepen, zerno, desc, int(price), V))
            self.add_status = True
        except Exception as e:
            self.add_status = False
            self.statusBar().showMessage("Неверно заполнена форма")
            print(e)
        else:
            self.con.commit()
            self.parent().update_table()
            self.close()

    def get_adding_verdict(self):
        return self.add_status


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.update_table()
        self.addButton.clicked.connect(self.adding)
        self.add_form = None

    def update_table(self):
        cur = self.con.cursor()
        que = "SELECT * FROM coffees"
        result = cur.execute(que).fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                                    'описание вкуса', 'цена', 'объем упаковки'])

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def adding(self):
        self.add_form = AddWidget(self)
        self.add_form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.exit(app.exec())
