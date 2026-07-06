#include <WiFi.h>
#include <WebServer.h>

// ==========================
// WIFI SETTINGS
// ==========================
const char* ssid = "YOUR_HOTSPOT_NAME";
const char* password = "YOUR_HOTSPOT_PASSWORD";

WebServer server(80);

// ==========================
// MOTOR PINS
// ==========================

// LEFT DRIVER
#define IN1 13
#define IN2 12
#define IN3 14
#define IN4 27

// RIGHT DRIVER
#define IN5 26
#define IN6 25
#define IN7 33
#define IN8 32

// ==========================

void stopMotors() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);

  digitalWrite(IN5, LOW);
  digitalWrite(IN6, LOW);
  digitalWrite(IN7, LOW);
  digitalWrite(IN8, LOW);
}

void forward() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  digitalWrite(IN5, HIGH);
  digitalWrite(IN6, LOW);
  digitalWrite(IN7, HIGH);
  digitalWrite(IN8, LOW);
}

void backward() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  digitalWrite(IN5, LOW);
  digitalWrite(IN6, HIGH);
  digitalWrite(IN7, LOW);
  digitalWrite(IN8, HIGH);
}

void left() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  digitalWrite(IN5, HIGH);
  digitalWrite(IN6, LOW);
  digitalWrite(IN7, HIGH);
  digitalWrite(IN8, LOW);
}

void right() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  digitalWrite(IN5, LOW);
  digitalWrite(IN6, HIGH);
  digitalWrite(IN7, LOW);
  digitalWrite(IN8, HIGH);
}

// ==========================

void handleRoot() {

  String page =
  "<!DOCTYPE html><html><head>"
  "<title>VisionRover</title>"
  "<meta name='viewport' content='width=device-width,initial-scale=1'>"
  "</head><body style='font-family:Arial;text-align:center;'>"

  "<h1>VisionRover Robot</h1>"

  "<p><a href='/forward'><button style='width:180px;height:60px;font-size:20px;'>FORWARD</button></a></p>"

  "<p>"
  "<a href='/left'><button style='width:100px;height:60px;'>LEFT</button></a> "

  "<a href='/stop'><button style='width:100px;height:60px;'>STOP</button></a> "

  "<a href='/right'><button style='width:100px;height:60px;'>RIGHT</button></a>"
  "</p>"

  "<p><a href='/backward'><button style='width:180px;height:60px;font-size:20px;'>BACKWARD</button></a></p>"

  "</body></html>";

  server.send(200, "text/html", page);
}

// ==========================

void setup() {

  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(IN5, OUTPUT);
  pinMode(IN6, OUTPUT);
  pinMode(IN7, OUTPUT);
  pinMode(IN8, OUTPUT);

  stopMotors();

  Serial.println();
  Serial.println("--------------------------------");
  Serial.println("Connecting to WiFi...");
  Serial.println("--------------------------------");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("--------------------------------");
  Serial.println("WiFi Connected!");
  Serial.print("Robot IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println("--------------------------------");

  server.on("/", handleRoot);

  server.on("/forward", []() {
    forward();
    server.send(200, "text/plain", "FORWARD");
  });

  server.on("/backward", []() {
    backward();
    server.send(200, "text/plain", "BACKWARD");
  });

  server.on("/left", []() {
    left();
    server.send(200, "text/plain", "LEFT");
  });

  server.on("/right", []() {
    right();
    server.send(200, "text/plain", "RIGHT");
  });

  server.on("/stop", []() {
    stopMotors();
    server.send(200, "text/plain", "STOP");
  });

  server.on("/ui", handleRoot);

  server.begin();

  Serial.println("HTTP Server Started");
}

void loop() {

  server.handleClient();
}