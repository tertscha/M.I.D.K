#include "MatrixMiniR4.h"

void setup()
{
  MiniR4.begin();
  MiniR4.PWR.setBattCell(2);
  Serial.begin(9600);
  MiniR4.I2C4.MXLaserV2.begin();
}

void loop()
{
  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(10, 10);
  MiniR4.OLED.print(MiniR4.I2C4.MXLaserV2.getDistance());
  MiniR4.OLED.display();
  if(MiniR4.I2C4.MXLaserV2.getDistance() < 100)
  {
    MiniR4.OLED.setCursor(10, 20);
    MiniR4.OLED.print("stop");
    MiniR4.OLED.display();
  }
  delay(100);

}
