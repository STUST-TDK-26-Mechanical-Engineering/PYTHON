#include <AutoPID.h>
#include <Wire.h>
#define  I2C_ADDRESS 0x50 //主機位置
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
uint8_t opcode; // register
uint8_t speed;  // fan speed: 0=off, 150=low, 200=medium, 250=high
volatile double input, setPoint, outputVal;
AutoPID myPID(&input, &setPoint, &outputVal, OUTPUT_MIN, OUTPUT_MAX, KP, KI, KD);
void init_i(){
  pinMode(DO1,INPUT);
  pinMode(DO2,INPUT);
  pinMode(DO3,INPUT);
  pinMode(DO4,INPUT);
  pinMode(RDO1,INPUT);
  pinMode(RDO2,INPUT);
  pinMode(RDO3,INPUT);
  pinMode(RDO4,INPUT);
}
void setup() {
  Serial.begin(9600);                       
  init_i();
  // myPID.setBangBang(4);
  myPID.setTimeStep(10);
  Wire.begin(I2C_ADDRESS);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
  setPoint=0;  
} 
int pid_val=0;
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
  myPID.run(); //call every loop, updates automatically at certain time interval
  if (!digitalRead(DO2)){
    input+=1;
  }
  if (!digitalRead(DO1)){
    input+=2;
  }
  if (!digitalRead(DO3)){
    input-=1;
  }if (!digitalRead(DO4)){
    input-=2;
  }
  if(!digitalRead(DO1)&&digitalRead(DO2)&&digitalRead(DO3)&&!digitalRead(DO4)){
    myPID.reset();
    input=0;
    outputVal=0;
  }
  Serial.print(outputVal);
  Serial.print("\t");
  Serial.print(input);
  Serial.print("\t");
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
  Serial.print("\n");
  delay(1);
}
void receiveEvent(int bytes) {
  //讀取第一個字節以確定涉及哪個寄存器
  opcode = Wire.read();
  // Serial.println(opcode);
  // 如果超過 1 個字節，則主機正在寫入從機
  
  if (bytes > 1) {
   
    if (opcode == 0x08){
      speed = Wire.read();  
      myPID.reset();
      input=0;
      outputVal=0;
      Serial.println("res");
      // Wire.write(4);
      // delay(500);
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
  int val =floor(outputVal);
  int low = 0x00ff & val;
  int high = (0xff00 & val) >> 8;
  data[1]=high;  
  data[2]=low;
  // Serial.print(sizeof(speed));
  if (opcode == 0x05) {
    for (int i = 0; i < 4; i++) {
      Wire.write((uint8_t *)&data[i],sizeof(data[i]));
      // Serial.println(data[i]);
    }
    // Wire.write((uint8_t *)&speed, sizeof(speed));
  }else {
    delay(5000);
    Wire.write(3);
  }
}
