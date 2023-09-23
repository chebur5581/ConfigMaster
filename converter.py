from settings import default_script, libraries, modes


class Script():
    def __init__(self, pins, defines=None, libraries=None, serial=None):
        self.pins = pins
        self.defines = defines
        self.libs = libraries
        self.serial = serial

        splitter = '\n'
        self.script = [e + splitter for e in default_script.split(splitter)]

        # prepare pins, заменяем ключи на их названия в define'ах
        if self.defines is not None:
            for name in self.defines:
                self.pins[self.defines[name]] = self.pins.pop(f'{name}')

    @property
    def to_str(self):
        return ''.join(self.script)

    @property
    def to_list(self):
        return self.script

    def compile(self, filename=None):
        # libs
        # добавляем все include'ы и то что нудно для инициализации либы
        if self.libs is not None:
            for lib in enumerate(self.libs):  # добавляем все include'ы и то что нудно для инициализации либы
                self.script[lib[0]] = libraries[lib[1]][0] + '\n'
                self.script.insert(lib[0] + 1, '\n')
                self.script.insert(lib[0] + 2, libraries[lib[1]][1] + '\n')

        # defines
        if self.defines is not None:
            for line in enumerate(self.script):
                if line[1] == '\n':
                    for define in self.defines:
                        self.script.insert(line[0] + 1, f'#define {self.defines[define]} {define}\n')
                    self.script.insert(line[0] + len(self.defines) + 1, '\n')
                    break

        # добавляем пустую строку перед сетапом
        setup_index = 0  # заранее запомним куда будем записывать pinMode'ы
        for line in enumerate(self.script):
            if 'void setup()' in line[1]:
                self.script.insert(line[0], '\n')
                setup_index = line[0] + 2
                break
        # pins
        working_index = 0  # индекс куда мы добавляем новый строки
        for pin in enumerate(self.pins):
            mode = self.pins[pin[1]][0]  # 0 - none, 1 - INPUT, 2 - OUTPUT
            if mode != 0:
                self.script.insert(working_index + setup_index, f'\tpinMode({pin[1]}, {modes[mode]});\n')
                working_index += 1
        # serial
        if self.serial is not None:
            self.script.insert(working_index + setup_index, '\n')
            self.script.insert(working_index + setup_index + 1, f'\tSerial.begin({self.serial});')

        # save to file
        if filename is not None:
            with open(filename, 'w') as f:
                f.write(''.join(self.script))

if __name__ == "__main__":
    pins = {'A0': [0, 2],  # [состояние 0-2, индекс комбобокса в tableWidget, ссылка на кнопку]
            'A1': [1, 3],
            'A2': [0, 4],
            'A3': [0, 5],
            'A4': [0, 6],
            'A5': [0, 7],
            '0': [0, 8],
            '1': [0, 9],
            '2': [1, 10],
            '3': [2, 11],
            '4': [1, 12],
            '5': [2, 13],
            '6': [0, 14],
            '7': [0, 15],
            '8': [0, 16],
            '9': [0, 17],
            '10': [0, 18],
            '11': [0, 19],
            '12': [0, 20],
            '13': [0, 21],
            }

    libs = ['lcd', 'servo']

    defs = {2: 'RS',
            3: 'D7',
            5: 'LED',
            'A1': 'POT'}

    c = Script(pins, defs, libs, serial=9600)
    c.compile('output.ino')
