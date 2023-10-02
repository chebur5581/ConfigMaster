import json
from sys import exit

from PyQt6.QtCore import QPoint, Qt, QRect, QRegularExpression as QRegExp
from PyQt6.QtGui import QIcon, QMouseEvent, QCursor, QRegularExpressionValidator as QRegExpValidator
from PyQt6.QtWidgets import QMainWindow, QApplication, QLineEdit, QComboBox, QPushButton, QFileDialog, QLabel, \
    QMessageBox, QTreeWidgetItem

from converter import Script
from gui import MainWindow
from logger import log
from settings import icons


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.ui.configure()  # Доп. добавки в ui которые не сделать через QtDesigner

        self.pins = self.ui.pins
        self.libs_pos = self.ui.libs_pos

        self.defines = {}
        self.libs = []
        self.script = None

        self.libs_links = {'lcd': self.ui.lcd,
                           'servo': self.ui.servo}
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
        self.ui.actionSave_2.triggered.connect(self.save_file)
        self.ui.action_Save_2.triggered.connect(self.save_file)
        self.ui.actionOpen.triggered.connect(self.open_file)

        self.ui.lcd.clicked.connect(lambda x: self.include_lib(self.ui.lcd))
        self.ui.servo.clicked.connect(lambda x: self.include_lib(self.ui.servo))

        self.ui.treeWidget.itemDoubleClicked.connect(self.load_example)

        self.offset = self.ui.frame_3.pos()
        self.old_pos = QPoint(0, 0)
        self.cur_pos = QPoint(0, 0)

    def load_example(self, i=QTreeWidgetItem, col=int):
        text = i.text(col)
        if text == 'ЖК-экран (LCD)':
            self.open_file('examples/lcd.cfmex')
        if text == 'Сервопривод':
            self.open_file('examples/servo.cfmex')

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self,
                                                  "Save File", "", "ConfigMaster Files(*.cfm)")
        if filename:
            self.save(filename)
            log('Saving completed', 'success')
            log(f'Path to file {filename}', 'info')

    def save(self, filename):
        libs = []
        for key in self.libs_pos.keys():
            pin = self.libs_pos[key]['pin']
            if pin is not None:
                for key_pin in self.pins.keys():
                    if pin == self.pins[key_pin][3]:
                        pin = key_pin
                        break
            libs.append({'pin': pin, 'pos': (key.x(), key.y())})

        serial = self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(1, 1)).currentIndex()
        dump = json.dumps({'pins': [i[0] for i in self.pins.values()],
                           'includes': self.libs,
                           'defs': self.defines,
                           'libs': libs,
                           'serial': serial})

        with open(filename, 'w') as f:
            f.write(dump)

    def open_file(self, filename):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self,
                                                      "Open File", "", "ConfigMaster Files(*.cfm)")
        if filename:
            with open(filename, 'r') as f:
                file = f.read()

            load = json.loads(file)
            for key in enumerate(self.pins.keys()):  # pin states
                self.pins[key[1]][0] = load['pins'][key[0]]
                self.change_mode(self.pins[key[1]][2], add=False)

            includes = load['includes']
            self.ui.servo.setChecked(False)
            self.ui.lcd.setChecked(False)
            if 'lcd' in includes:
                self.ui.lcd.setChecked(True)
            if 'servo' in includes:
                self.ui.servo.setChecked(True)
            self.include_lib(self.ui.servo)
            self.include_lib(self.ui.lcd)

            self.defines = load['defs']
            # log(load)
            for key in self.pins.keys():
                if key not in self.defines:
                    self.pins[key][3].setText('')
                    self.pins[key][3].setStyleSheet('QLineEdit{background-color: rgba(255, 255, 255, 0);}')
                else:
                    self.pins[key][3].setText(self.defines[key])

            for i in enumerate(self.libs_pos.keys()):
                pin = load['libs'][i[0]]['pin']
                if pin is not None:
                    self.libs_pos[i[1]]['pin'] = self.pins[pin][3]
                    self.pins[pin][3].setStyleSheet('QLineEdit{background-color: rgba(255, 255, 255, 0);border: none;}')
                else:
                    self.libs_pos[i[1]]['pin'] = None

                pos = load['libs'][i[0]]['pos']
                i[1].move(pos[0], pos[1])
                self.libs_pos[i[1]]['offset'] = QPoint(pos[0], pos[1])

            self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(1, 1)).setCurrentIndex(load['serial'])
            log(f'{filename} successfully loaded', 'success')

    def new_file(self):  # [состояние 0-2, индекс комбобокса в tableWidget, ссылка на кнопку]
        for key in self.pins.keys():  # clear pin modes
            self.pins[key][0] = 0
            self.change_mode(self.pins[key][2], add=False)
            self.pins[key][3].clear()

        self.ui.lcd.setChecked(False)
        self.ui.servo.setChecked(False)

        self.include_lib(self.ui.lcd)
        self.include_lib(self.ui.servo)

        self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(1, 1)).setCurrentIndex(0)

    def include_lib(self, button: QPushButton):
        if button.isChecked():
            self.libs.append(button.objectName())

            if button.objectName() == 'lcd':
                for but in self.libs_buttons['lcd']:
                    but.show()
            else:
                self.ui.LibServo.show()

        if not button.isChecked() and button.objectName() in self.libs:
            self.libs.remove(button.objectName())

            if button.objectName() == 'lcd':
                for but in self.libs_buttons['lcd']:
                    but.hide()
            else:
                self.ui.LibServo.hide()

    def compile(self):

        if 'servo' in self.libs:
            if self.libs_pos[self.ui.LibServo]['pin'] is None:
                QMessageBox.critical(self, 'Error', 'Подключены не все пины для библиотек',
                                     QMessageBox.StandardButton.Ok)
                return 0
        elif 'lcd' in self.libs:
            for key in self.libs_buttons['lcd']:
                if self.libs_pos[key]['pin'] is None:
                    QMessageBox.critical(self, 'Error', 'Подключены не все пины для библиотек',
                                         QMessageBox.StandardButton.Ok)
                    return 0

        bod = self.ui.tableWidget.indexWidget(self.ui.tableWidget.model().index(1, 1)).currentText()
        if bod == 'Выключить':
            bod = None

        self.script = Script(pins=self.pins, defines=self.defines, libraries=self.libs, serial=bod)

        filename, _ = QFileDialog.getSaveFileName(self,
                                                  "Save File", "", "Arduino Files(*.ino)")
        if filename:
            self.script.compile(filename)
            log('compile completed', 'success')
            log(f'saved in {filename}', 'info')

    def definition(self, lineEdit: QLineEdit):
        reg_ex = QRegExp("[\w-]+")
        input_validator = QRegExpValidator(reg_ex, lineEdit)
        lineEdit.setValidator(input_validator)

        key = lineEdit.objectName().replace('L', '')  # Ключь - пин на подобии A0 A1
        value = lineEdit.text().replace(' ', '')  # текст для названия пина
        self.defines.update({key: value})  # добавляем в словарь
        table_index = self.pins[key][1]  # получаем индекс пина в таблице
        if value == '':  # если текст стёрли
            self.defines.pop(key)  # удаляем пин из словаря
            self.ui.tableWidget.item(table_index, 0).setText(f'          pin {key}')  # ставим текст
        else:
            self.ui.tableWidget.item(table_index, 0).setText(f'pin {value} ({key})')  # ставим текст

        for key in self.libs_pos.keys():
            # если значение лайна меняется то сбрасываем значки и состояния
            if self.libs_pos[key]['pin'] == lineEdit:
                lineEdit.setStyleSheet('QLineEdit{background-color: rgba(255, 255, 255, 0);}')
                key.move(self.libs_pos[key]['default'])
                self.libs_pos[key]['pin'] = None
                if lineEdit.text() == '':
                    self.libs_pos[key]['offset'] = key.pos()
        if lineEdit.text() == ' ':
            lineEdit.clear()

    def mode_changed(self, c_box: QComboBox):  # Если значение комбокса изменилось, то меняем его везде
        pin = c_box.objectName().replace('pin', '').replace('P', '')
        button = self.pins.get(pin)[2]  # получаем объект кнопки соответствующий комбоксу
        value = c_box.currentIndex()  # индекс выбранной строки
        self.pins[pin][0] = value  # устанавливаем значение от 0 до 2
        button.setIcon(QIcon(icons.get(value)))  # ставим иконку input/output/none

    def libPressEvent(self, lib=QLabel, e=QMouseEvent):
        self.libs_pos[lib]['old'] = e.pos()  # всё тоже что и у frame_3

    def libMoveEvent(self, lib=QLabel, e=QMouseEvent):
        self.libs_pos[lib]['cur'] = e.pos()  # всё тоже что и у frame_3
        offset = self.libs_pos[lib]['cur'] - self.libs_pos[lib]['old']
        lib.move(offset + self.libs_pos[lib]['offset'])

    def libReleaseEvent(self, lib=QLabel, e=QMouseEvent):
        for item in self.pins.keys():  # всё тоже что и у frame_3 почти
            lineEdit = self.pins[item][3]  # получаем лайн едит

            # получаем глобальные координаты родительского виджета
            global_pos = lineEdit.parentWidget().mapToGlobal(QPoint())

            # получаем его ширину и высоту
            w, h = lineEdit.parentWidget().width(), lineEdit.parentWidget().height()
            cur = QCursor.pos()  # позиция курсора

            # квадрат для определения находиться ли мышка над ним
            rect = QRect(global_pos.x(), global_pos.y(), w, h)
            if rect.contains(cur):  # проверка
                # перемещаем значёк либы на место виджета
                lib.move(self.ui.frame_3.mapFromGlobal(global_pos))
                # ставим текст
                lineEdit.setText(lib.objectName().replace('Lib', '').upper())
                # убираем бортики
                lineEdit.setStyleSheet('QLineEdit{border: none;}')
                # добавляем в словарь
                self.libs_pos[lib]['pin'] = lineEdit

                self.pins[item][0] = 0
                self.change_mode(self.pins[item][2], add=False)
                break

        self.libs_pos[lib]['offset'] = lib.pos()  # сохраняем смещение

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
                    self.libReleaseEvent(lib, e)
                    break

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.RightButton:
            self.cur_pos = e.pos()
            offset = self.cur_pos - self.old_pos
            self.ui.frame_3.move(self.offset + offset)
        else:
            for lib in self.libs_pos.keys():
                if lib.underMouse():
                    lineEdit = self.libs_pos[lib]['pin']
                    if lineEdit is not None:
                        lineEdit.setText(' ')
                        lineEdit.setStyleSheet('QLineEdit{background-color: rgba(255, 255, 255, 0);}')
                    self.libMoveEvent(lib, e)
                    break

    def change_mode(self, button: QPushButton, add=True):  # input, output, none
        name = button.objectName().replace('P', '')  # получаем имя кнопки
        value = self.pins.get(name)[0]  # получаем значение кнопки от 0 до 2
        # log(value)
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
