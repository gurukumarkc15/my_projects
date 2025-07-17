// Motor pins
#define AIN1 4
#define AIN2 3
#define PWMA 9
#define STBY 5
#define BIN1 6
#define BIN2 7
#define PWMB 10

// Sensor pins
#define SENSOR_COUNT 7
const int sensorPins[SENSOR_COUNT] = {A0, A1, A2, A3, A4, A5, A6};
int sensorValues[SENSOR_COUNT];
int threshold = 470; // Adjust based on sensor characteristics (for now 470)

void setup() {
  // Initialize motor control pins
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(STBY, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(PWMB, OUTPUT);

  // Initialize standby pin
  digitalWrite(STBY, HIGH);

  // Initialize sensor pins
  for (int i = 0; i < SENSOR_COUNT; i++) {
    pinMode(sensorPins[i], INPUT);
  }

  // Initialize Serial communication
  Serial.begin(9600);
}

void loop() {
  // Read sensor values
  for (int i = 0; i < SENSOR_COUNT; i++) {
    sensorValues[i] = analogRead(sensorPins[i]);
  }

  // Print sensor values
  Serial.print("Sensor values: ");
  for (int i = 0; i < SENSOR_COUNT; i++) {
    Serial.print(sensorValues[i]);
    if (i < SENSOR_COUNT - 1) {
      Serial.print(", ");
    }
  }
  Serial.println();

  // Initialize variables for direction control
  bool leftDetected = false;
  bool rightDetected = false;
  bool centerDetected = false;

  // Detect line based on sensor readings
  for (int i = 0; i < SENSOR_COUNT; i++) {
    if (sensorValues[i] > threshold) {
      if (i < SENSOR_COUNT / 2) {
        leftDetected = true;
      } else if (i > SENSOR_COUNT / 2) {
        rightDetected = true;
      } else {
        centerDetected = true;
      }
    }
  }

  // Control motor movement based on detected line position
  if (centerDetected) {
    // Move forward
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMA, 255); // Full speed
    analogWrite(PWMB, 255); // Full speed
  } else if (leftDetected) {
    // Turn right
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMA, 255); // Full speed
    analogWrite(PWMB, 0);   // Stop right motor
  } else if (rightDetected) {
    // Turn left
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, LOW);
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMA, 0);   // Stop left motor
    analogWrite(PWMB, 255); // Full speed
  } else {
    // Stop
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, LOW);
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMA, 0);
    analogWrite(PWMB, 0);
  }

  // Small delay to avoid flooding the serial monitor
  delay(1000);
}
