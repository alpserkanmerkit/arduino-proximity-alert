/*
  proximity-alert v1 (simple) — Alp Serkan Merkit, MIT License

  Reconstructed line by line from a screen recording of the original sketch
  (Arduino IDE 2.3.5, board: Arduino Uno). Code is kept exactly as it
  appears in the video (the original Turkish comments are translated to English); only line breaks were normalised where several
  statements were captured on one transcribed line.
  The one part that could not be read is marked [UNREADABLE] below.

  Zones (cm):  <= 5 red LED + fan ON  |  5-15 "yellow" LED blinks  |  > 15 green LED
  On the breadboard the LED on pin 5 ("yellowLed") is physically a BLUE LED.
*/

// Pin definitions
const int trigPin = 9;     // Sensor Trig pin
const int echoPin = 10;    // Sensor Echo pin
const int redLed = 3;      // Red LED
const int yellowLed = 5;   // Yellow LED
const int greenLed = 6;    // Green LED
const int motorPin = 11;   // Motor pin

// Variables
long duration;             // Duration of the sound wave
int distance;              // Calculated distance
int stableDistance;        // More stable distance

void setup() {
  // Set up the pins
  // [UNREADABLE] The individual pinMode() lines are not legible in the video.
  // The six lines below are completed from the pin list above (OUTPUT/INPUT as used in loop()).
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(redLed, OUTPUT);
  pinMode(yellowLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(motorPin, OUTPUT);

  // For communication with the computer
  Serial.begin(9600);
}

void loop() {
  // Measure distance with the sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2; // Distance (cm)

  // Stabilize the distance
  stableDistance = (stableDistance * 0.7) + (distance * 0.3);

  // Show the distance on the computer
  Serial.print("Mesafe: ");
  Serial.print(stableDistance);
  Serial.println(" cm");

  // What happens based on the distance?
  if (stableDistance <= 5) {          // 0-5 cm (close range)
    digitalWrite(motorPin, HIGH);     // Motor runs
    digitalWrite(redLed, HIGH);       // Red lights up
    digitalWrite(yellowLed, LOW);
    analogWrite(greenLed, 0);
  }
  else if (stableDistance <= 15) {    // 5-15 cm (medium range)
    digitalWrite(motorPin, LOW);      // Motor stops
    digitalWrite(redLed, LOW);
    digitalWrite(yellowLed, HIGH);    // Yellow lights up
    delay(200);                       // Wait 0.2 seconds
    digitalWrite(yellowLed, LOW);
    delay(200);
    analogWrite(greenLed, 0);
  }
  else {                              // More than 15 cm (far range)
    digitalWrite(motorPin, LOW);      // Motor stops
    digitalWrite(redLed, LOW);
    digitalWrite(yellowLed, LOW);
    analogWrite(greenLed, 255);       // Green lights up
  }
}
