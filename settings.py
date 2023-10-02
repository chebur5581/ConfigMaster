# пути к иконкам
icons = {0: 'assets/none.png', 1: 'assets/input.png', 2: 'assets/output.png'}

label_scales = []

default_script = '''
void setup() {

}

void loop() {

}
'''

modes = {1: 'INPUT', 2: 'OUTPUT', 3: 'INPUT_PULLUP'}

logging = True
debug = True

libraries = {
    'lcd': ['#include <LiquidCrystal.h>', 'LiquidCrystal lcd(RS, E, D4, D5, D6, D7); // укажите нужные вам пины'],
    'servo': ['#include <Servo.h>', 'Servo myservo; // можно и не myservo', 'myservo.attach(pin);']}
