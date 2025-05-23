#include "driver/ledc.h"

// === Sensor Setup ===
const int sensorPins[8] = { 36, 39, 34, 35, 32, 33, 25, 26 };
int weights[8] = { -3500, -2500, -1500, -500, 500, 1500, 2500, 3500 };
int sensorMin[8] = { 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500 };
int sensorMax[8] = { 4095, 4095, 4095, 4095, 4095, 4095, 4095, 4095 };

// === L9110S Motor Pins (ESP32 PWM-compatible) ===
const int A_IA = 23;  // Left motor
const int A_IB = 22;
const int B_IA = 19;  // Right motor
const int B_IB = 18;

// === Motor PWM Channels ===
const int CH_A_IA = 0;
const int CH_A_IB = 1;
const int CH_B_IA = 2;
const int CH_B_IB = 3;

const int PWM_FREQ = 1000;     // 1kHz PWM frequency
const int PWM_RESOLUTION = 8;  // 8-bit resolution (0-255)

// === PID Variables ===
float Kp = 0.5;
float Ki = 0.0;
float Kd = 0.1;

float error = 0, lastError = 0, integral = 0;
int baseSpeed = 150;

void setup() {
  Serial.begin(115200);

  // Set up PWM channels
  ledcAttachChannel(A_IA, PWM_FREQ, PWM_RESOLUTION, CH_A_IA);
  ledcAttachChannel(A_IB, PWM_FREQ, PWM_RESOLUTION, CH_A_IB);
  ledcAttachChannel(B_IA, PWM_FREQ, PWM_RESOLUTION, CH_B_IA);
  ledcAttachChannel(B_IB, PWM_FREQ, PWM_RESOLUTION, CH_B_IB);

  // Attach PWM channels to pins
  // ledcAttachPin(A_IA, CH_A_IA);
  // ledcAttachPin(A_IB, CH_A_IB);
  // ledcAttachPin(B_IA, CH_B_IA);
  // ledcAttachPin(B_IB, CH_B_IB);

  // Initialize sensor min/max
  // for (int i = 0; i < 8; i++) {
  //   pinMode(sensorPins[i], INPUT);
  //   sensorMin[i] = 1023;
  //   sensorMax[i] = 0;
  // }

  // === Auto Calibration ===
  // Serial.println("Calibrating sensors... Move robot over the line.");
  // unsigned long startTime = millis();
  // while (millis() - startTime < 5000) {
  //   for (int i = 0; i < 8; i++) {
  //     int raw = analogRead(sensorPins[i]);
  //     sensorMin[i] = min(sensorMin[i], raw);
  //     sensorMax[i] = max(sensorMax[i], raw);
  //   }
  //   delay(50);
  // }
  // Serial.println("Calibration complete.");
}

void loop() {
  int sensorValues[8];
  long weightedSum = 0;
  long total = 0;
  int position = 0;

  for (int i = 0; i < 8; i++) {
    int raw = analogRead(sensorPins[i]);
    sensorMin[i] = min(sensorMin[i], raw);
    sensorMax[i] = max(sensorMax[i], raw);

    int calibrated = constrain(map(raw, sensorMin[i], sensorMax[i], 0, 1000), 0, 1000);
    sensorValues[i] = calibrated;

    weightedSum += (long)calibrated * weights[i];
    total += calibrated;
  }

  if (total > 0)
    position = weightedSum / total;
  else
    position = 0;

  // === PID Control ===
  error = position;
  integral += error;
  float derivative = error - lastError;
  float correction = Kp * error + Ki * integral + Kd * derivative;
  lastError = error;

  int leftSpeed = constrain(baseSpeed - correction, 0, 255);
  int rightSpeed = constrain(baseSpeed + correction, 0, 255);

  // === Motor Control with ESP32 PWM ===
  setL9110Motor(CH_A_IA, CH_A_IB, leftSpeed, true);   // Left motor forward
  setL9110Motor(CH_B_IA, CH_B_IB, rightSpeed, true);  // Right motor forward

  // === Debug Output ===
  Serial.print("Pos: ");
  Serial.print(position);
  Serial.print(" | L: ");
  Serial.print(leftSpeed);
  Serial.print(" R: ");
  Serial.println(rightSpeed);

  delay(10);
}

void setL9110Motor(int chA, int chB, int speed, bool forward) {
  if (forward) {
    ledcWrite(chA, speed);
    ledcWrite(chB, 0);
  } else {
    ledcWrite(chA, 0);
    ledcWrite(chB, speed);
  }
}