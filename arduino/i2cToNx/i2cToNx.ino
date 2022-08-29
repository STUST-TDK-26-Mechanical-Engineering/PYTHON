#include <Wire.h>

uint8_t opcode; // register
uint8_t speed;  // fan speed: 0=off, 150=low, 200=medium, 250=high
#define FAN_DC_MOTOR_PIN 3
#define  I2C_ADDRESS 0x42
#define REGISTER_POWER 0x01
#define REGISTER_SPEED 0x02
void setup() {
  Serial.begin(9600);
  pinMode(FAN_DC_MOTOR_PIN, OUTPUT);
  Wire.begin(I2C_ADDRESS);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
}

void loop() {
  // Move the DC motor at a given speed
  analogWrite(FAN_DC_MOTOR_PIN, speed);
  delay(1000);
}

void receiveEvent(int bytes) {
  // Read the first byte to determine which register is concerned
  opcode = Wire.read();
  Serial.println(opcode);
  // If there are more than 1 byte, then the master is writing to the slave
  if (bytes > 1) {
    if (opcode == REGISTER_SPEED) {
      speed = Wire.read();
      Serial.println(speed);
      Serial.println("0x01");
    } else if (opcode == REGISTER_POWER) {
      speed = (Wire.read() == 1) ? 200 /* on */ : 0 /* off */;
    }
  }
}

void requestEvent() {
  // Read from the register variable to know what to send back
  
  if (opcode == REGISTER_SPEED) {
    Wire.write((uint8_t *)&speed, sizeof(speed));
  } else {
    Wire.write(3);
  }
}