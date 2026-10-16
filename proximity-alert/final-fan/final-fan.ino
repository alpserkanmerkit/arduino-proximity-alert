/*
  proximity-alert FINAL (propeller fan) — Alp Serkan Merkit, MIT License

  Reconstructed 2026 from the owner's description; original sketch not preserved.

  What the owner describes for the final build: the propeller speed follows the distance zone
      red  (near)   -> fan stops
      blue (medium) -> fan fast
      green (far)   -> fan slow
  Everything else below is ASSUMED and can be changed:
    - pins: same wiring as v1-simple.ino (assumed; not visible in footage):
      TRIG 9, ECHO 10, red 3, blue 5, green 6, motor 11
    - zone borders: 5 cm and 15 cm (the v1 values)
    - FAN_SLOW / FAN_FAST: PWM values 0-255; tune them on your motor
      (a small motor may not start below ~100: raise FAN_SLOW until it spins)
    - the LEDs are steady here; the description gives the colours, not blink patterns
  D11 never drives the motor directly: it drives a transistor (recommended: TIP120 + 1N4007 +
  its own battery, see docs/wiring-final-fan.png). Serial Monitor: 9600 baud, "Mesafe: N cm".
*/

const int trigPin  = 9;    // HC-SR04 TRIG
const int echoPin  = 10;   // HC-SR04 ECHO
const int redLed   = 3;    // near
const int blueLed  = 5;    // medium ("yellowLed" in v1/v2; the LED on the board is blue)
const int greenLed = 6;    // far
const int motorPin = 11;   // PWM -> 1 kOhm -> transistor base

const int NEAR_CM  = 5;
const int MEDIUM_CM = 15;
const int FAN_SLOW = 120;  // far zone
const int FAN_FAST = 255;  // medium zone

int stableDistance = 100;  // start "far" so the fan does not jump at power-up

int measureCm() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH, 30000UL);   // 30 ms timeout
  if (duration == 0) return 400;                     // no echo = far away
  return duration * 0.034 / 2;
}

void show(int red, int blue, int green, int fan) {
  digitalWrite(redLed, red);
  digitalWrite(blueLed, blue);
  digitalWrite(greenLed, green);
  analogWrite(motorPin, fan);
}

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(redLed, OUTPUT);
  pinMode(blueLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(motorPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  stableDistance = stableDistance * 0.7 + measureCm() * 0.3;   // same noise filter as v1
  Serial.print("Mesafe: ");
  Serial.print(stableDistance);
  Serial.println(" cm");

  if (stableDistance <= NEAR_CM) {
    show(HIGH, LOW, LOW, 0);          // red: fan stops
  } else if (stableDistance <= MEDIUM_CM) {
    show(LOW, HIGH, LOW, FAN_FAST);   // blue: fan fast
  } else {
    show(LOW, LOW, HIGH, FAN_SLOW);   // green: fan slow
  }
  delay(60);                          // HC-SR04: at least ~60 ms between pings
}
