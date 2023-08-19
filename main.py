from PyQt6 import QtWidgets, QtCore, QtGui

from gui import MainWindow
from settings import *
import sys


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.ui.configure()  # доп. добавки в ui

        self.ui.A0.clicked.connect(lambda x: self.change_mode(self.ui.A0))
        self.ui.A1.clicked.connect(lambda x: self.change_mode(self.ui.A1))
        self.ui.A2.clicked.connect(lambda x: self.change_mode(self.ui.A2))
        self.ui.A3.clicked.connect(lambda x: self.change_mode(self.ui.A3))
        self.ui.A4.clicked.connect(lambda x: self.change_mode(self.ui.A4))
        self.ui.A5.clicked.connect(lambda x: self.change_mode(self.ui.A5))

    def change_mode(self, button):  # input, output, none
        name = button.objectName()  # получаем имя кнопки
        value = pins.get(name)  # получаем значение кнопки от 0 до 2
        print(f'{name}: {value}')
        if value == 2:
            pins[name] = 0
        elif value < 2:
            pins[name] += 1
        button.setIcon(QtGui.QIcon(icons.get(value)))  # установка иконки по номеру
        # 0 - none
        # 1 - input
        # 2 - output



if __name__ == "__main__":  # запуск всего
    app = QtWidgets.QApplication([])
    application = App()
    application.show()
    sys.exit(app.exec())
