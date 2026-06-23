#define D1_IN1 13
#define D1_IN2 12
#define D1_IN3 14
#define D1_IN4 27

#define D2_IN1 26
#define D2_IN2 25
#define D2_IN3 33
#define D2_IN4 32

void stopMotors() {
  digitalWrite(D1_IN1, LOW);
  digitalWrite(D1_IN2, LOW);
  digitalWrite(D1_IN3, LOW);
  digitalWrite(D1_IN4, LOW);

  digitalWrite(D2_IN1, LOW);
  digitalWrite(D2_IN2, LOW);
  digitalWrite(D2_IN3, LOW);
  digitalWrite(D2_IN4, LOW);
}

void forward() {
  digitalWrite(D1_IN1, HIGH);
  digitalWrite(D1_IN2, LOW);
  digitalWrite(D1_IN3, HIGH);
  digitalWrite(D1_IN4, LOW);

  digitalWrite(D2_IN1, HIGH);
  digitalWrite(D2_IN2, LOW);
  digitalWrite(D2_IN3, HIGH);
  digitalWrite(D2_IN4, LOW);
}

void backward() {
  digitalWrite(D1_IN1, LOW);
  digitalWrite(D1_IN2, HIGH);
  digitalWrite(D1_IN3, LOW);
  digitalWrite(D1_IN4, HIGH);

  digitalWrite(D2_IN1, LOW);
  digitalWrite(D2_IN2, HIGH);
  digitalWrite(D2_IN3, LOW);
  digitalWrite(D2_IN4, HIGH);
}

void setup() {
  pinMode(D1_IN1, OUTPUT);
  pinMode(D1_IN2, OUTPUT);
  pinMode(D1_IN3, OUTPUT);
  pinMode(D1_IN4, OUTPUT);

  pinMode(D2_IN1, OUTPUT);
  pinMode(D2_IN2, OUTPUT);
  pinMode(D2_IN3, OUTPUT);
  pinMode(D2_IN4, OUTPUT);

  stopMotors();
}

void loop() {
  forward();
  delay(3000);

  stopMotors();
  delay(1000);

  backward();
  delay(3000);

  stopMotors();
  delay(1000);
}