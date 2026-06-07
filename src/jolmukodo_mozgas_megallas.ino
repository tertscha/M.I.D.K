#include <MatrixMiniR4.h>

int baseSpeed = 5;
float Kp = 0.1;

double targetYaw = 0;
bool running = false;

const int stopDistanceMM = 100;

unsigned long startTime = 0;

void stopRobot() {
  MiniR4.M3.setSpeed(0);
  MiniR4.M4.setSpeed(0);

  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(0, 0);
  MiniR4.OLED.print("STOP");
  MiniR4.OLED.display();
}

void setup() {
  MiniR4.begin();
  MiniR4.I2C1.MXLaserV2.begin();

  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(0, 0);
  MiniR4.OLED.print("Calibrating...");
  MiniR4.OLED.display();

  delay(1000);

  MiniR4.Motion.resetIMUValues();
  delay(500);

  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(0, 0);
  MiniR4.OLED.print("Ready");
  MiniR4.OLED.display();
}

void loop() {

  if (MiniR4.BTN_DOWN.getState()) {
    running = true;
    startTime = millis();

    targetYaw = MiniR4.Motion.getEuler(MiniR4Motion::AxisType::Yaw);

    MiniR4.OLED.clearDisplay();
    MiniR4.OLED.setCursor(0, 0);
    MiniR4.OLED.print("RUN");
    MiniR4.OLED.display();

    delay(300);
  }

  if (MiniR4.BTN_UP.getState()) {
    running = false;
    stopRobot();
    delay(300);
  }

  if (!running) {
    return;
  }

  uint16_t distance = MiniR4.I2C1.MXLaserV2.getDistance();

  if (distance > 0 && distance < stopDistanceMM) {
    running = false;

    MiniR4.M3.setSpeed(0);
    MiniR4.M4.setSpeed(0);

    MiniR4.OLED.clearDisplay();
    MiniR4.OLED.setCursor(0, 0);
    MiniR4.OLED.print("OBSTACLE");
    MiniR4.OLED.display();

    return;
  }

  double yaw = MiniR4.Motion.getEuler(MiniR4Motion::AxisType::Yaw);

  double error = targetYaw - yaw;
  double correction = error * Kp;
  correction = constrain(correction, -1.0, 1.0);

  int m3Speed = baseSpeed - correction;
  int m4Speed = baseSpeed + correction;

  // M4 indulási rásegítés
  if (millis() - startTime < 500) {
    m4Speed += 4;
  }

  m3Speed = constrain(m3Speed, -20, 20);
  m4Speed = constrain(m4Speed, -20, 20);

  MiniR4.M3.setSpeed(m3Speed);
  MiniR4.M4.setSpeed(m4Speed);

  delay(30);
}
