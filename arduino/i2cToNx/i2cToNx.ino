#include <Wire.h>

uint8_t opcode; // register
uint8_t speed;  // fan speed: 0=off, 150=low, 200=medium, 250=high
#define FAN_DC_MOTOR_PIN 3
#define  I2C_ADDRESS 0x42 //主機位置
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

}

void receiveEvent(int bytes) {
  //讀取第一個字節以確定涉及哪個寄存器
  opcode = Wire.read();
  // Serial.println(opcode);
  // 如果超過 1 個字節，則主機正在寫入從機
  if (bytes > 1) {
    if (opcode == REGISTER_SPEED) {
      speed = Wire.read();
      Serial.println(speed);
      Serial.println(opcode);
    } else if (opcode == REGISTER_POWER) {
      speed = (Wire.read() == 1) ? 200 /* on */ : 0 /* off */;
    }
  }
}

void requestEvent() {
  // Read from the register variable to know what to send back
  Serial.print("Event");
  // Serial.print(sizeof(speed));
  if (opcode == REGISTER_SPEED) {
    Wire.write((uint8_t *)&speed, sizeof(speed));
  } else {
    delay(5000);
    // Wire.write(3);
  }
}