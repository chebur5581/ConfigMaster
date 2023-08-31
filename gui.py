from main_gui import Ui_MainWindow


class MainWindow(Ui_MainWindow):
    def configure(self):
        # установка виджетов в tableWidget
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(1, 1), self.bod)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(2, 1), self.pinA0)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(3, 1), self.pinA1)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(4, 1), self.pinA2)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(5, 1), self.pinA3)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(6, 1), self.pinA4)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(7, 1), self.pinA5)

        self.tableWidget.setIndexWidget(self.tableWidget.model().index(8, 1), self.pin0)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(9, 1), self.pin1)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(10, 1), self.pin2)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(11, 1), self.pin3)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(12, 1), self.pin4)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(13, 1), self.pin5)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(14, 1), self.pin6)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(15, 1), self.pin7)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(16, 1), self.pin8)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(17, 1), self.pin9)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(18, 1), self.pin10)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(19, 1), self.pin11)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(20, 1), self.pin12)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(21, 1), self.pin13)

