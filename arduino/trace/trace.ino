#include <AutoPID.h>
#include <Wire.h>
#include <math.h>
#define I2C_ADDRESS 0x50  //主機位置
#define DO1 5
#define DO2 4
#define DO3 3
#define DO4 2
#define RDO1 6
#define RDO2 7
#define RDO3 8
#define RDO4 9

#define OUTPUT_MIN -255
#define OUTPUT_MAX 255
#define KP 1
#define KI 0.003
#define KD 0

#define Z_OUTPUT_MIN -500
#define Z_OUTPUT_MAX 500
#define Z_KP 1
#define Z_KI 1
#define Z_KD 0
volatile bool stale = false;
uint8_t opcode;  // register
uint8_t speed;   // fan speed: 0=off, 150=low, 200=medium, 250=high
volatile double input, setPoint, outputVal;
volatile double Z_input, Z_setPoint, Z_outputVal;
AutoPID myPID(&input, &setPoint, &outputVal, OUTPUT_MIN, OUTPUT_MAX, KP, KI, KD);
AutoPID Z_myPID(&Z_input, &Z_setPoint, &Z_outputVal, Z_OUTPUT_MIN, Z_OUTPUT_MAX, Z_KP, Z_KI, Z_KD);
void init_i() {
  pinMode(DO1, INPUT);
  pinMode(DO2, INPUT);
  pinMode(DO3, INPUT);
  pinMode(DO4, INPUT);
  pinMode(RDO1, INPUT);
  pinMode(RDO2, INPUT);
  pinMode(RDO3, INPUT);
  pinMode(RDO4, INPUT);
}
void setup() {
  Serial.begin(9600);
  init_i();
  // myPID.setBangBang(4);
  myPID.setTimeStep(100);
  Z_myPID.setTimeStep(100);
  Wire.begin(I2C_ADDRESS);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
  Wire.setWireTimeout(13000 /* us */, true /* reset_on_timeout */);
  setPoint = 0;
}
int pid_val = 0;
void yData(){
  if (!digitalRead(DO1)) {
    input += 2;
  }
  if (!digitalRead(DO2)) {
    input += 1;
  }
  if (!digitalRead(DO3)) {
    input -= 1;
  }
  if (!digitalRead(DO4)) {
    input -= 2;
  }
  if (!digitalRead(DO1) && digitalRead(DO2) && digitalRead(DO3) && !digitalRead(DO4)) {
    myPID.reset();
    input = 0;
    outputVal = 0;
  }
}
void zData(){
  if(digitalRead(DO2)&&digitalRead(DO3)){
    if (!digitalRead(RDO1)) {
      Z_input -= 10;
    }
    if (!digitalRead(RDO2)) {
      Z_input -= 5;
    }
    if (!digitalRead(RDO3)) {
      Z_input += 5;
    }
    if (!digitalRead(RDO4)) {
      Z_input += 10;
    }
  }
  
  if (!digitalRead(RDO1) && digitalRead(RDO2) && digitalRead(RDO3) && !digitalRead(RDO4)) {
    Z_myPID.reset();
    Z_input = 0;
    Z_outputVal = 0;
  }
}
void loop() {
  // int val = 500;
  // int low = 0x00ff & val;
  // int high = (0xff00 & val) >> 8;
  // Serial.print(String(val, HEX));
  // Serial.print("\t");
  // Serial.print(String(low, HEX));
  // Serial.print("\t");
  // Serial.print(String(high, HEX));
  // Serial.println("\t");
  // String(-500, HEX);
  myPID.run();  //call every loop, updates automatically at certain time interval
  Z_myPID.run();
  yData();
  zData();
  // Serial.print(outputVal);
  // Serial.print("\t");
  // Serial.print(input);
  // Serial.print("\t");
  // Serial.print(stale);
  // Serial.print("\t");
  // Serial.print(Z_outputVal);
  // Serial.print("\t");
  // Serial.print(Z_input);
  // Serial.print("\t");
 
  // Serial.print(digitalRead(DO1));
  // Serial.print("\t");
  // Serial.print(digitalRead(DO2));
  // Serial.print("\t");
  // Serial.print(digitalRead(DO3));
  // Serial.print("\t");
  // Serial.print(digitalRead(DO4));
  // Serial.println("\t");
  // Serial.print(digitalRead(RDO1));
  // Serial.print("\t");
  // Serial.print(digitalRead(RDO2));
  // Serial.print("\t");
  // Serial.print(digitalRead(RDO3));
  // Serial.print("\t");
  // Serial.print(digitalRead(RDO4));
  // Serial.print("\n");
  delay(30);
}
void receiveEvent(int bytes) {
  //讀取第一個字節以確定涉及哪個寄存器
  opcode = Wire.read();
  Serial.println(String(opcode, HEX));
  // 如果超過 1 個字節，則主機正在寫入從機

  if (bytes > 1) {

    if (opcode == 0x03) {//歸零
      speed = Wire.read();
      // speed = Wire.read();
      myPID.reset();
      Z_myPID.reset();
      input = 0;
      outputVal = 0;
      Z_input = 0;
      Z_outputVal = 0;
      // stale = true;
      Serial.println(speed);
      // Wire.write(4);
      // delay(500);
    }else if(opcode == 0x08){//初始化設定
      int y1 = Wire.read();
      int y2=Wire.read();
      int z1=Wire.read();
      int z2=Wire.read();
      Serial.print(y1);
      Serial.print("\t");
      Serial.println(y2);
      Serial.print(z1);
      Serial.print("\t");
      Serial.println(z2);
      int y_ouput=y1*pow(16,2)+y2;
      int z_ouput=z1*pow(16,2)+z2;
      if (y1>128){
        y1=255-y1;
        y2=256-y2;
        y_ouput=-(y1*pow(16,2)+y2);
      }
      if (z1>128){
        z1=255-z1;
        z2=256-z2;
        z_ouput=-(z1*pow(16,2)+z2);
      }
      input= y_ouput; 
      Z_input= z_ouput;        
      Serial.println(y_ouput);
      Serial.println(z_ouput);      
    }
    // if (opcode == REGISTER_SPEED) {
    //   speed = Wire.read();
    //   Serial.println(speed);
    //   Serial.println(opcode);
    // } else if (opcode == REGISTER_POWER) {
    //   speed = (Wire.read() == 1) ? 200 /* on */ : 0 /* off */;
    // }
  }
}
byte data[4];
void requestEvent() {
  // Read from the register variable to know what to send back
  // Serial.println("Event");
  // Serial.println(opcode);
  int val = floor(outputVal);
  int low = 0x00ff & val;
  int high = (0xff00 & val) >> 8;

  int Z_val = floor(Z_outputVal);
  int Z_low = 0x00ff & Z_val;
  int Z_high = (0xff00 & Z_val) >> 8;
  data[0] = high;
  data[1] = low;
  data[2] = Z_high;
  data[3] = Z_low;
  // Serial.print(sizeof(speed));
  if (opcode == 0x01) {
    for (int i = 0; i < 4; i++) {
      Wire.write((uint8_t *)&data[i], sizeof(data[i]));
      // Serial.println(data[i]);
    }
    // Wire.write((uint8_t *)&speed, sizeof(speed));
  } else {
    delay(5000);
    Wire.write(3);
  }
}