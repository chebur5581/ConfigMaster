from main_gui import Ui_MainWindow


# Крч в main_gui.py не лезть, он автоматом создаётся
# если что-то надо добавить в ui то добавлять в сюда в MainWindow

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

        self.tableWidget.setIndexWidget(self.tableWidget.model().index(8, 1), self.pinP0)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(9, 1), self.pinP1)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(10, 1), self.pinP2)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(11, 1), self.pinP3)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(12, 1), self.pinP4)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(13, 1), self.pinP5)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(14, 1), self.pinP6)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(15, 1), self.pinP7)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(16, 1), self.pinP8)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(17, 1), self.pinP9)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(18, 1), self.pinP10)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(19, 1), self.pinP11)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(20, 1), self.pinP12)
        self.tableWidget.setIndexWidget(self.tableWidget.model().index(21, 1), self.pinP13)

