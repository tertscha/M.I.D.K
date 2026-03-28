
#include <WiFiS3.h>
#include <MatrixMiniR4.h>   // ha ezt használod a motorokhoz

char ssid[] = "EDE-WAN-C";
char pass[] = "Linksys2011";
int speed = 10;
WiFiServer server(80);

// ====== Itt tedd a saját motorvezérlő függvényeidet ======
void stopRobot() {
  // pl. motor stop
  Serial.println("STOP");
        // STOP
  MiniR4.M3.setSpeed(0);
  MiniR4.M4.setSpeed(0);
  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(10, 0);
  MiniR4.OLED.print("STOP");
  MiniR4.OLED.display();
}

void goForward() {
  // pl. bal motor előre, jobb motor előre
  Serial.println("FORWARD");
  // ELŐRE
  MiniR4.M3.setSpeed(speed);
  MiniR4.M4.setSpeed(speed);
  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(10, 0);
  MiniR4.OLED.print("Forward");
  MiniR4.OLED.display(); 
}

void goBackward() {
  Serial.println("BACKWARD");
 // HÁTRA
  MiniR4.M3.setSpeed(speed * -1);
  MiniR4.M4.setSpeed(speed * -1);
  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(10, 0);
  MiniR4.OLED.print("Backwards");
  MiniR4.OLED.display();
}

void turnLeft() {
  Serial.println("LEFT");
   // BALRA
  MiniR4.M3.setSpeed(speed);
  MiniR4.M4.setSpeed(speed * -1);
  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(10, 0);
  MiniR4.OLED.print("Left");
  MiniR4.OLED.display();
} 

void turnRight() {
  Serial.println("RIGHT");
  // JOBRA
  MiniR4.M3.setSpeed(speed * -1);
  MiniR4.M4.setSpeed(speed);
  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(10, 0);
  MiniR4.OLED.print("Right");
  MiniR4.OLED.display();
}
// =========================================================

void setup() {
  Serial.begin(115200);
  delay(1500);

  // Ha a Matrix könyvtárad igényli, itt init:
  MiniR4.begin();

  Serial.print("Csatlakozás a WiFi-re: ");
  Serial.println(ssid);

  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    Serial.println("Nem sikerült, újrapróbálás 3 mp múlva...");
    delay(3000);
  }

  Serial.println("WiFi csatlakozva.");
  Serial.print("Robot IP címe: ");
  Serial.println(WiFi.localIP());
  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(20, 0);
  MiniR4.OLED.print(WiFi.localIP());
  MiniR4.OLED.display(); 

  server.begin();
  Serial.println("Webszerver elindult.");
}

void sendPage(WiFiClient &client) {
  client.println("HTTP/1.1 200 OK");
  client.println("Content-type:text/html; charset=utf-8");
  client.println("Connection: close");
  client.println();

  client.println("<!DOCTYPE html><html><head>");
  client.println("<meta name='viewport' content='width=device-width, initial-scale=1'>");
  client.println("<style>");
  client.println("body{font-family:Arial;text-align:center;margin-top:30px;}");
  client.println("button{width:120px;height:60px;font-size:20px;margin:8px;}");
  client.println("</style></head><body>");
  client.println("<h2>Matrix Mini R4 robot irányítás</h2>");
  client.println("<p><a href='/forward'><button>Előre</button></a></p>");
  client.println("<p>");
  client.println("<a href='/left'><button>Balra</button></a>");
  client.println("<a href='/stop'><button>Stop</button></a>");
  client.println("<a href='/right'><button>Jobbra</button></a>");
  client.println("</p>");
  client.println("<p><a href='/backward'><button>Hátra</button></a></p>");
  client.println("</body></html>");
}

void loop() {
  int distance = MiniR4.I2C4.MXLaserV2.getDistance();

  if (distance > 0 && distance < 100) {
    stopRobot();
  }
  WiFiClient client = server.available();
  if (!client) return;

  String request = "";
  unsigned long timeout = millis();

  while (client.connected() && millis() - timeout < 1000) {
    if (client.available()) {
      char c = client.read();
      request += c;
      if (c == '\n') break;  // első sor elég
    }
  }

  Serial.println("Kérés:");
  Serial.println(request);

  if (request.indexOf("GET /forward") >= 0) {
    goForward();
  } else if (request.indexOf("GET /backward") >= 0) {
    goBackward();
  } else if (request.indexOf("GET /left") >= 0) {
    turnLeft();
  } else if (request.indexOf("GET /right") >= 0) {
    turnRight();
  } else if (request.indexOf("GET /stop") >= 0) {
    stopRobot();
  }

  sendPage(client);
  delay(1);
  client.stop();
}
