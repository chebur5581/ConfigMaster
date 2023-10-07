from PyQt6.QtCore import QPoint

from main_gui import Ui_MainWindow


# Крч в main_gui.py не лезть, он автоматом создаётся
# если что-то надо добавить в ui то добавлять в сюда в MainWindow

class MainWindow(Ui_MainWindow):
    def configure(self):

        self.toolBar.setStyleSheet('QToolBar{background-color: rgb(255, 255, 255);border: 1px solid grey; border-top: none;}')

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

        self.autoTrace.hide()

        # [состояние 0-2, индекс комбобокса в tableWidget, ссылка на кнопку, ссылка на LineEdit]
        self.pins = {'A0': [0, 2,  self.A0, self.LA0],
                     'A1': [0, 3,  self.A1, self.LA1],
                     'A2': [0, 4,  self.A2, self.LA2],
                     'A3': [0, 5,  self.A3, self.LA3],
                     'A4': [0, 6,  self.A4, self.LA4],
                     'A5': [0, 7,  self.A5, self.LA5],
                     '0': [0, 8,   self.P0, self.L0],
                     '1': [0, 9,   self.P1, self.L1],
                     '2': [0, 10,  self.P2, self.L2],
                     '3': [0, 11,  self.P3, self.L3],
                     '4': [0, 12,  self.P4, self.L4],
                     '5': [0, 13,  self.P5, self.L5],
                     '6': [0, 14,  self.P6, self.L6],
                     '7': [0, 15,  self.P7, self.L7],
                     '8': [0, 16,  self.P8, self.L8],
                     '9': [0, 17,  self.P9, self.L9],
                     '10': [0, 18, self.P10, self.L10],
                     '11': [0, 19, self.P11, self.L11],
                     '12': [0, 20, self.P12, self.L12],
                     '13': [0, 21, self.P13, self.L13],
                     }

        self.libs_pos = {self.LibRs: {'offset':  self.LibRs.pos().__pos__(),
                                      'old':     QPoint(0, 0),
                                      'cur':     QPoint(0, 0),
                                      'default': self.LibRs.pos(),
                                      'pin':     None},

                         self.LibE: {'offset':   self.LibE.pos().__pos__(),
                                     'old':      QPoint(0, 0),
                                     'cur':      QPoint(0, 0),
                                     'default':  self.LibE.pos(),
                                     'pin': None},

                         self.LibD4: {'offset':  self.LibD4.pos().__pos__(),
                                      'old':     QPoint(0, 0),
                                      'cur':     QPoint(0, 0),
                                      'default': self.LibD4.pos(),
                                      'pin':     None},

                         self.LibD5: {'offset':  self.LibD5.pos().__pos__(),
                                      'old':     QPoint(0, 0),
                                      'cur':     QPoint(0, 0),
                                      'default': self.LibD5.pos(),
                                      'pin':     None},

                         self.LibD6: {'offset':  self.LibD6.pos().__pos__(),
                                      'old':     QPoint(0, 0),
                                      'cur':     QPoint(0, 0),
                                      'default': self.LibD6.pos(),
                                      'pin':     None},

                         self.LibD7: {'offset':  self.LibD7.pos().__pos__(),
                                      'old':     QPoint(0, 0),
                                      'cur':     QPoint(0, 0),
                                      'default': self.LibD7.pos(),
                                      'pin':     None},

                         self.LibServo: {'offset':  self.LibServo.pos().__pos__(),
                                         'old':     QPoint(0, 0),
                                         'cur':     QPoint(0, 0),
                                         'default': self.LibServo.pos(),
                                         'pin':     None}
                         }
