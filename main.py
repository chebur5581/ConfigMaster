from sys import exit

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import QMainWindow, QApplication, QLineEdit, QComboBox, QPushButton, QFileDialog, QLabel

from converter import Script
from gui import MainWindow
from settings import icons


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.ui.configure()  # Доп. добавки в ui которые не сделать через QtDesigner

        self.defines = {}
        self.libs = []
        self.script = None

        self.libs_buttons = {'lcd': [self.ui.LibRs,
                                     self.ui.LibE,
                                     self.ui.LibD4,
                                     self.ui.LibD5,
                                     self.ui.LibD6,
                                     self.ui.LibD7],
                             'servo': self.ui.LibServo}

        self.buttons_and_combos()  # мне стыдно за это

        self.ui.actionCompile.triggered.connect(self.compile)
        self.ui.actionCompile_2.triggered.connect(self.compile)
        self.ui.action_New.triggered.connect(self.new_file)

        self.ui.lcd.clicked.connect(lambda x: self.include_lib(self.ui.lcd))
        self.ui.servo.clicked.connect(lambda x: self.include_lib(self.ui.servo))

        self.offset = self.ui.frame_3.pos()
        self.old_pos = QPoint(0, 0)
        self.cur_pos = QPoint(0, 0)

        # [состояние 0-2, индекс комбобокса в tableWidget, ссылка на кнопку]
        self.pins = {'A0': [0, 2, self.ui.A0, self.ui.LA0],
                     'A1': [0, 3, self.ui.A1, self.ui.LA1],
                     'A2': [0, 4, self.ui.A2, self.ui.LA2],
                     'A3': [0, 5, self.ui.A3, self.ui.LA3],
                     'A4': [0, 6, self.ui.A4, self.ui.LA4],
                     'A5': [0, 7, self.ui.A5, self.ui.LA5],
                     '0': [0, 8, self.ui.P0, self.ui.L0],
                     '1': [0, 9, self.ui.P1, self.ui.L1],
                     '2': [0, 10, self.ui.P2, self.ui.L2],
                     '3': [0, 11, self.ui.P3, self.ui.L3],
                     '4': [0, 12, self.ui.P4, self.ui.L4],
                     '5': [0, 13, self.ui.P5, self.ui.L5],
                     '6': [0, 14, self.ui.P6, self.ui.L6],
                     '7': [0, 15, self.ui.P7, self.ui.L7],
                     '8': [0, 16, self.ui.P8, self.ui.L8],
                     '9': [0, 17, self.ui.P9, self.ui.L9],
                     '10': [0, 18, self.ui.P10, self.ui.L10],
                     '11': [0, 19, self.ui.P11, self.ui.L11],
                     '12': [0, 20, self.ui.P12, self.ui.L12],
                     '13': [0, 21, self.ui.P13, self.ui.L13],
                     }
        self.libs_pos = {self.ui.LibRs: {'offset': self.ui.LibRs.pos().__pos__(),
                                         'old': QPoint(0, 0),
                                         'cur': QPoint(0, 0)},
                         self.ui.LibE: {'offset': self.ui.LibE.pos().__pos__(),
                                        'old': QPoint(0, 0),
                                        'cur': QPoint(0, 0)},
                         self.ui.LibD4: {'offset': self.ui.LibD4.pos().__pos__(),
                                         'old': QPoint(0, 0),
                                         'cur': QPoint(0, 0)},
                         self.ui.LibD5: {'offset': self.ui.LibD5.pos().__pos__(),
                                         'old': QPoint(0, 0),
                                         'cur': QPoint(0, 0)},
                         self.ui.LibD6: {'offset': self.ui.LibD6.pos().__pos__(),
                                         'old': QPoint(0, 0),
                                         'cur': QPoint(0, 0)},
                         self.ui.LibD7: {'offset': self.ui.LibD7.pos().__pos__(),
                                         'old': QPoint(0, 0),
                                         'cur': QPoint(0, 0)},
                         self.ui.LibServo: {'offset': self.ui.LibServo.pos().__pos__(),
                                            'old': QPoint(0, 0),
                                            'cur': QPoint(0, 0)}
                         }

    # def wheelEvent(self, e):
    #     self.ui.frame_3.wheelEvent(e)
    #     self.zoom = e.angleDelta().y() //

    def new_file(self):  # [состояние 0-2, индекс комбобокса в tableWidget, ссылка на кнопку]
        for key in self.pins.keys():
            self.pins[key][0] = 0
            self.change_mode(self.pins[key][2], add=False)
            self.pins[key][3].clear()

        self.ui.lcd.setChecked(False)
        self.ui.servo.setChecked(False)

        self.include_lib(self.ui.lcd)
        self.include_lib(self.ui.servo)

    def include_lib(self, button: QPushButton):
        if button.isChecked():
            self.libs.append(button.objectName())

            if button.objectName() == 'lcd':
                for but in self.libs_buttons['lcd']:
                    but.show()
            else:
                self.ui.LibServo.show()

        if not button.isChecked():
            self.libs.remove(button.objectName())

            if button.objectName() == 'lcd':
                for but in self.libs_buttons['lcd']:
                    but.hide()
            else:
                self.ui.LibServo.hide()

    def compile(self):
        bod = self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(1, 1)).currentText()
        if bod == 'Выключить':
            bod = None

        self.script = Script(pins=self.pins, defines=self.defines, libraries=self.libs, serial=bod)

        filename, _ = QFileDialog.getSaveFileName(self,
                                                  "Save File", "", "Arduino Files(*.ino)")
        if filename:
            self.script.compile(filename)
            print('compile completed')
            print(f'saved in {filename}')

    def definition(self, lineEdit: QLineEdit):
        key = lineEdit.objectName().replace('L', '')  # Ключь - пин на подобии A0 A1
        value = lineEdit.text()  # текст для названия пина
        self.defines.update({key: value})  # добавляем в словарь
        table_index = self.pins[key][1]  # получаем индекс пина в таблице
        if value == '':  # если текст стёрли
            self.defines.pop(key)  # удаляем пин из словаря
            self.ui.tableWidget.item(table_index, 0).setText(f'          pin {key}')  # ставим текст
        else:
            self.ui.tableWidget.item(table_index, 0).setText(f'pin {value} ({key})')  # ставим текст

    def mode_changed(self, c_box: QComboBox):  # Если значение комбокса изменилось, то меняем его везде
        pin = c_box.objectName().replace('pin', '').replace('P', '')
        button = self.pins.get(pin)[2]  # получаем объект кнопки соответствующий комбоксу
        value = c_box.currentIndex()  # индекс выбранной строки
        self.pins[pin][0] = value  # устанавливаем значение от 0 до 2
        button.setIcon(QIcon(icons.get(value)))  # ставим иконку input/output/none

    def libPressEvent(self, lib=QLabel, e=QMouseEvent):
        self.libs_pos[lib]['old'] = e.pos()
        print(self.libs_pos[lib]['old'])
        print('press')

    def libMoveEvent(self, lib=QLabel, e=QMouseEvent):
        self.libs_pos[lib]['cur'] = e.pos()
        offset = self.libs_pos[lib]['cur'] - self.libs_pos[lib]['old']
        lib.move(offset + self.libs_pos[lib]['offset'])
        print(self.libs_pos[lib]['cur'])
        print(offset)
        print('move')

    def libReleaseEvent(self, lib=QLabel):
        self.libs_pos[lib]['offset'] += self.libs_pos[lib]['cur'] - self.libs_pos[lib]['old']
        print(self.libs_pos[lib]['offset'])
        print('release')

    def mousePressEvent(self, e=QMouseEvent):
        if e.button() == Qt.MouseButton.RightButton:
            self.old_pos = e.pos()
        else:
            for lib in self.libs_pos.keys():
                if lib.underMouse():
                    self.libPressEvent(lib, e)
                    break

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton and self.old_pos != e.pos():
            self.offset += self.cur_pos - self.old_pos
        else:
            for lib in self.libs_pos.keys():
                if lib.underMouse():
                    self.libReleaseEvent(lib)
                    break

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.RightButton:
            self.cur_pos = e.pos()
            offset = self.cur_pos - self.old_pos
            self.ui.frame_3.move(self.offset + offset)
        else:
            for lib in self.libs_pos.keys():
                if lib.underMouse():
                    self.libMoveEvent(lib, e)
                    break

    def change_mode(self, button: QPushButton, add=True):  # input, output, none
        name = button.objectName().replace('P', '')  # получаем имя кнопки
        value = self.pins.get(name)[0]  # получаем значение кнопки от 0 до 2
        print(value)
        if value == 2 and add:  # тут всё понятно прибавляем значение пока оно не станет ровно 2 потом сбрасываем до 0
            self.pins[name][0] = 0
        if value < 2 and add:
            self.pins[name][0] += 1

        value = self.pins.get(name)[0]  # обновляем value

        index = self.pins.get(name)[1]  # номер строки на которой находиться комбокс для пина
        self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(index, 1)).setCurrentIndex(value)
        # ^^^ установка нужной строки по индексу ^^^

        button.setIcon(QIcon(icons.get(value)))  # установка иконки input/output/none

        # 0 - none
        # 1 - input
        # 2 - output

    def buttons_and_combos(self):
        # говорим что если кнопка нажата то вызвать функцию change_mode и передать себя как аргумент
        self.ui.LibServo.hide()
        for but in self.libs_buttons['lcd']:
            but.hide()

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

        self.ui.LA0.textChanged.connect(lambda x: self.definition(self.ui.LA0))
        self.ui.LA1.textChanged.connect(lambda x: self.definition(self.ui.LA1))
        self.ui.LA2.textChanged.connect(lambda x: self.definition(self.ui.LA2))
        self.ui.LA3.textChanged.connect(lambda x: self.definition(self.ui.LA3))
        self.ui.LA4.textChanged.connect(lambda x: self.definition(self.ui.LA4))
        self.ui.LA5.textChanged.connect(lambda x: self.definition(self.ui.LA5))

        self.ui.L0.textChanged.connect(lambda x: self.definition(self.ui.L0))
        self.ui.L1.textChanged.connect(lambda x: self.definition(self.ui.L1))
        self.ui.L2.textChanged.connect(lambda x: self.definition(self.ui.L2))
        self.ui.L3.textChanged.connect(lambda x: self.definition(self.ui.L3))
        self.ui.L4.textChanged.connect(lambda x: self.definition(self.ui.L4))
        self.ui.L5.textChanged.connect(lambda x: self.definition(self.ui.L5))
        self.ui.L6.textChanged.connect(lambda x: self.definition(self.ui.L6))
        self.ui.L7.textChanged.connect(lambda x: self.definition(self.ui.L7))
        self.ui.L8.textChanged.connect(lambda x: self.definition(self.ui.L8))
        self.ui.L9.textChanged.connect(lambda x: self.definition(self.ui.L9))
        self.ui.L10.textChanged.connect(lambda x: self.definition(self.ui.L10))
        self.ui.L11.textChanged.connect(lambda x: self.definition(self.ui.L11))
        self.ui.L12.textChanged.connect(lambda x: self.definition(self.ui.L12))
        self.ui.L13.textChanged.connect(lambda x: self.definition(self.ui.L13))

        # если значение комбокса изменилось, то вызывем функцию mode_changed и передаём себя
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
    app = QApplication([])
    application = App()
    application.show()
    exit(app.exec())
