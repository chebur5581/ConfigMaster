from PyQt6 import QtWidgets, QtGui

from gui import MainWindow
from settings import *
import sys


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.ui.configure()  # доп. добавки в ui которые не сделать через QtDesigner

        self.buttons_and_combos()  # мне стыдно за это

        self.pins = {'A0': [1, 2, self.ui.A0],  # [состояние 0-2, индекс комбобокса в tableWidget, ссылка на кнопку]
                     'A1': [1, 3, self.ui.A1],
                     'A2': [1, 4, self.ui.A2],
                     'A3': [1, 5, self.ui.A3],
                     'A4': [1, 6, self.ui.A4],
                     'A5': [1, 7, self.ui.A5],
                     'P0': [1, 8, self.ui.P0],
                     'P1': [1, 9, self.ui.P1],
                     'P2': [1, 10, self.ui.P2],
                     'P3': [1, 11, self.ui.P3],
                     'P4': [1, 12, self.ui.P4],
                     'P5': [1, 13, self.ui.P5],
                     'P6': [1, 14, self.ui.P6],
                     'P7': [1, 15, self.ui.P7],
                     'P8': [1, 16, self.ui.P8],
                     'P9': [1, 17, self.ui.P9],
                     'P10': [1, 18, self.ui.P10],
                     'P11': [1, 19, self.ui.P11],
                     'P12': [1, 20, self.ui.P12],
                     'P13': [1, 21, self.ui.P13],
                     }

    def mode_changed(self, c_box):  # если значение комбокса изменилось то меняем его везде
        pin = c_box.objectName().replace('pin', '')
        button = self.pins.get(pin)[2]  # получаем объект кнопки соответствующий комбоксу
        value = c_box.currentIndex()  # индекс выбранной строки
        self.pins[pin][0] = value  # устанавливаем значение от 0 до 2
        button.setIcon(QtGui.QIcon(icons.get(value)))  # ставим иконку input/output/none

    def change_mode(self, button):  # input, output, none
        name = button.objectName()  # получаем имя кнопки
        value = self.pins.get(name)[0]  # получаем значение кнопки от 0 до 2

        index = self.pins.get(name)[1]  # номер строки на которой находиться комбокс для пина
        self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(index, 1)).setCurrentIndex(value)
        # ^^^ установка нужной строки по индексу ^^^

        if value == 2:  # тут всё понятно прибавляем значение пока оно не станет ровно 2 потом сбрасываем до 0
            self.pins[name][0] = 0
        elif value < 2:
            self.pins[name][0] += 1

        button.setIcon(QtGui.QIcon(icons.get(value)))  # установка иконки input/output/none

        # 0 - none
        # 1 - input
        # 2 - output

    def buttons_and_combos(self):
        # говорим что если кнопка нажата то вызвать функцию change_mode и передать себя как аргумент
        self.ui.A0.clicked.connect(lambda x: self.change_mode(self.ui.A0))
        self.ui.A1.clicked.connect(lambda x: self.change_mode(self.ui.A1))
        self.ui.A2.clicked.connect(lambda x: self.change_mode(self.ui.A2))
        self.ui.A3.clicked.connect(lambda x: self.change_mode(self.ui.A3))
        self.ui.A4.clicked.connect(lambda x: self.change_mode(self.ui.A4))
        self.ui.A5.clicked.connect(lambda x: self.change_mode(self.ui.A5))

        self.ui.P0.clicked.connect(lambda x: self.change_mode(self.ui.P0))
        self.ui.P1.clicked.connect(lambda x: self.change_mode(self.ui.P1))
        self.ui.P2.clicked.connect(lambda x: self.change_mode(self.ui.P2))
        self.ui.P3.clicked.connect(lambda x: self.change_mode(self.ui.P3))
        self.ui.P4.clicked.connect(lambda x: self.change_mode(self.ui.P4))
        self.ui.P5.clicked.connect(lambda x: self.change_mode(self.ui.P5))
        self.ui.P6.clicked.connect(lambda x: self.change_mode(self.ui.P6))
        self.ui.P7.clicked.connect(lambda x: self.change_mode(self.ui.P7))
        self.ui.P8.clicked.connect(lambda x: self.change_mode(self.ui.P8))
        self.ui.P9.clicked.connect(lambda x: self.change_mode(self.ui.P9))
        self.ui.P10.clicked.connect(lambda x: self.change_mode(self.ui.P10))
        self.ui.P11.clicked.connect(lambda x: self.change_mode(self.ui.P11))
        self.ui.P12.clicked.connect(lambda x: self.change_mode(self.ui.P12))
        self.ui.P13.clicked.connect(lambda x: self.change_mode(self.ui.P13))

        # если значение комбокса изменилось то вызывем функцию mode_changed и передаём себя
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(2, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(2, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(3, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(3, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(4, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(4, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(5, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(5, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(6, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(6, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(7, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(7, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(8, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(8, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(9, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(9, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(10, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(10, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(11, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(11, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(12, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(12, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(13, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(13, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(14, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(14, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(15, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(15, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(16, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(16, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(17, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(17, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(18, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(18, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(19, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(19, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(20, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(20, 1))))
        self.ui.tableWidget.indexWidget(
            self.ui.tableWidget.model().index(21, 1)).currentIndexChanged.connect(
            lambda x: self.mode_changed(
                self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(21, 1))))


if __name__ == "__main__":  # запуск всего
    app = QtWidgets.QApplication([])
    application = App()
    application.show()
    sys.exit(app.exec())
