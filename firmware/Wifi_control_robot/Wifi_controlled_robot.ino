#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "VisionRover";
const char* password = "12345678";

WebServer server(80);

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

void handleRoot() {

  String page =
  "<html><body>"
  "<h1>VisionRover</h1>"

  "<p><a href='/forward'><button style='width:150px;height:60px;'>FORWARD</button></a></p>"

  "<p>"
  "<a href='/left'><button style='width:100px;height:60px;'>LEFT</button></a> "

  "<a href='/stop'><button style='width:100px;height:60px;'>STOP</button></a> "

  "<a href='/right'><button style='width:100px;height:60px;'>RIGHT</button></a>"
  "</p>"

  "<p><a href='/backward'><button style='width:150px;height:60px;'>BACKWARD</button></a></p>"

  "</body></html>";

  server.send(200, "text/html", page);
}

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

  WiFi.softAP(ssid, password);

  Serial.println("");
  Serial.println("WiFi Started");
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleRoot);

  server.on("/forward", []() {
    forward();
    handleRoot();
  });

  server.on("/backward", []() {
    backward();
    handleRoot();
  });

  server.on("/left", []() {
    left();
    handleRoot();
  });

  server.on("/right", []() {
    right();
    handleRoot();
  });

  server.on("/stop", []() {
    stopMotors();
    handleRoot();
  });

  server.begin();
}

void loop() {
  server.handleClient();
}