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
