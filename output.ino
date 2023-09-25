#include <LiquidCrystal.h>
#include <Servo.h>

#define POT A1
#define LED 5
#define D7 3
#define RS 2

Servo myservo; // можно и не myservo
LiquidCrystal lcd(RS, E, D4, D5, D6, D7); // укажите нужные вам пины

void setup() {
	pinMode(4, INPUT);
	pinMode(RS, INPUT);
	pinMode(D7, OUTPUT);
	pinMode(LED, OUTPUT);
	pinMode(POT, INPUT);

	Serial.begin(9600);
}

void loop() {

}

