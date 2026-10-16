/*
  proximity-alert v2 (advanced, 23.04.2025) — Alp Serkan Merkit, MIT License

  Source: a screen recording of the original sketch. Only original lines 58-93
  were legible; they are reproduced VERBATIM below between the
  "VERBATIM" markers (code verbatim; the original Turkish comments are translated to English). Low confidence: original lines 82-93
  (the loop() below) were read from one slightly blurred frame, so single characters may
  differ from the original. Everything outside those markers
  is COMPLETED to match the behaviour seen in the video:
    - averaging filter -> updateReadings() fills `average`
    - near:   closeRangeResponse()  (body not seen; completed like v1: fan + red on)
    - medium: yellow LED blinks, period = map(average, CLOSE_RANGE, MEDIUM_RANGE, 100, 500) ms
    - far:    fan/red/yellow off, green LED "breathes" (PWM fade in/out)
    - Serial "Mesafe: N cm" at 9600 baud
  Not seen in the video and therefore assumed: pin numbers (same as v1),
  CLOSE_RANGE / MEDIUM_RANGE values (v1 zone borders), filter length.
*/

// ======================= COMPLETED (not visible in the video) =======================
const int trigPin = 9;          // assumed: same wiring as v1
const int echoPin = 10;
const int redLedPin = 3;
const int yellowLedPin = 5;     // physically a blue LED on the breadboard
const int greenLedPin = 6;      // PWM pin (analogWrite)
const int motorPin = 11;        // fan: 1 k -> transistor base (recommended driver, see docs)

const int CLOSE_RANGE = 5;      // cm, value not visible -> v1 border
const int MEDIUM_RANGE = 15;    // cm, value not visible -> v1 border

const int NUM_READINGS = 5;     // averaging window, value not visible
int readings[NUM_READINGS];
int readIndex = 0;
long total = 0;
int average = 0;

int measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH, 30000UL);  // completed: 30 ms timeout
  if (duration == 0) return 400;                     // no echo -> treat as far away
  return duration * 0.034 / 2;
}

// Moving average of the last NUM_READINGS distances.
void updateReadings() {
  total -= readings[readIndex];
  readings[readIndex] = measureDistance();
  total += readings[readIndex];
  readIndex = (readIndex + 1) % NUM_READINGS;
  average = total / NUM_READINGS;
}

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(redLedPin, OUTPUT);
  pinMode(yellowLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
  pinMode(motorPin, OUTPUT);
  Serial.begin(9600);
  for (int i = 0; i < NUM_READINGS; i++) readings[i] = 0;
}

void closeRangeResponse() {
  digitalWrite(motorPin, HIGH);         // fan on
  digitalWrite(redLedPin, HIGH);
  digitalWrite(yellowLedPin, LOW);
  analogWrite(greenLedPin, 0);
}

void mediumRangeResponse() {
  digitalWrite(motorPin, LOW);          // completed: fan off in the medium zone
// ======================= VERBATIM: original lines 58-65 =======================
  digitalWrite(redLedPin, LOW);        // Red LED off   (line 58: only partly legible)
  int blinkDelay = map(average, CLOSE_RANGE, MEDIUM_RANGE, 100, 500);
  digitalWrite(yellowLedPin, HIGH);
  delay(blinkDelay);
  digitalWrite(yellowLedPin, LOW);
  delay(blinkDelay);
  analogWrite(greenLedPin, 0);         // Green LED off
}

// ======================= VERBATIM: original lines 67-93 =======================
// (lines 82-93 = loop(): low confidence, read from one blurred frame)
void farRangeResponse() {
  digitalWrite(motorPin, LOW);         // Motor off
  digitalWrite(redLedPin, LOW);        // Red LED off
  digitalWrite(yellowLedPin, LOW);     // Yellow LED off
  for (int brightness = 0; brightness <= 255; brightness += 5) {
    analogWrite(greenLedPin, brightness);
    delay(10);
  }
  for (int brightness = 255; brightness >= 0; brightness -= 5) {
    analogWrite(greenLedPin, brightness);
    delay(10);
  }
}

void loop() {
  updateReadings();
  Serial.print("Mesafe: ");
  Serial.print(average);
  Serial.println(" cm");
  if (average <= CLOSE_RANGE) {
    closeRangeResponse();
  } else if (average <= MEDIUM_RANGE) {
    mediumRangeResponse();
  } else {
    farRangeResponse();
  }
}
// ======================= END VERBATIM =======================
