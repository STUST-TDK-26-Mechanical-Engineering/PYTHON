// #include <TimerOne.h>//呼叫TimerOne函式庫
#include <Wire.h>
#include <EEPROM.h>
#define FR 9 //正反轉腳位(高電位正轉低電位反轉)  F/R
#define ST 10 //啟動馬達腳位(高電位停止低電位啟動) R/S 
#define Sp 11 //調轉速腳位 ADJ
#define BR 12 //煞車腳位(高電位放煞車低電位煞車) BRK
#define SG 2 //讀取訊號腳位 PLS(中斷控制)（脈波訊號接收）
// #define CL A5 //控制訊號腳位 可變電阻
#define limitSwitch 5//限位器腳位
#define  I2C_ADDRESS 0x42 //主機位置
#define EEPROM_MODE true //啟用EEPROM儲存資料（啟用後主轉速與最高角度將會以記憶體內為主，如需要修改請使用SetSped()/SetUpperLimit())
bool Correction=false;//用來判斷校正模式
uint8_t opcode; // register
uint8_t speed;  // fan speed: 0=off, 150=low, 200=medium, 250=high
int sped = 50;//設定轉速範圍0~255(0-5V)
int UpperLimit=10;//最高位置
/* 馬達驅動器COM 連接 Arduino GND*/
volatile int pulse = 0;//儲存馬達當前脈波數
volatile bool direction;//方向
void requestEvent();
void receiveEvent(int bytes);
void setup() {
  
  Serial.begin(9600);
  Serial.print(F("\n-------------initialization-------------"));
  pinMode(FR, OUTPUT);
  pinMode(ST, OUTPUT);
  pinMode(Sp, OUTPUT);
  pinMode(BR, OUTPUT);
  pinMode(SG, INPUT);
  pinMode(limitSwitch, INPUT);
  Wire.begin(I2C_ADDRESS);//初始化i2c
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
  attachInterrupt(digitalPinToInterrupt(SG), blink, FALLING);
  if(EEPROM_MODE){
    Serial.print("\nEEPROM_MODE:ON");
    EEPROM_init();    
  }else{
    Serial.print("\nEEPROM_MODE:OFF");
    Serial.print("\nUpperLimit:");
    Serial.print(UpperLimit);
    Serial.print("\nsped:");
    Serial.print(sped);    
  }
  Serial.print(F("\nI2C_ADDRESS:"));
  Serial.print(F("0x"));
  Serial.print(I2C_ADDRESS,HEX);
  Serial.println(F("\n---------end of initialization---------"));
}
void EEPROM_init(){
  UpperLimit=turn(EEPROM.read(0xA1));
  Serial.print("\nUpperLimit:");
  Serial.print(UpperLimit);
  sped=EEPROM.read(0xA2);
  Serial.print("\nsped:");
  Serial.print(sped);
}
void loop() {
}
int turn(int a)
{
	a = ~a + 1;
	return a;
}
/*##############
  #            #
  # 參數設定函式 #
  #            #
  #############*/

void SetSped(int val){//設定轉速
  Serial.print(F("\nSetSped:"));
  Serial.println(val);
  sped=val;
}
void SetUpperLimit(int val){//設定轉向最高位置
  Serial.print(F("\nSetUpperLimit:"));
  val=turn(val);//轉負數
  Serial.println(val);
  UpperLimit= val; 
}
//####################END#######################


/*#################################################
  #                                               #
  #            馬達轉控制主要函式                    #
  #                                               #
  #################################################*/
void blink() {
  if (!digitalRead(limitSwitch)){
    digitalWrite(BR, LOW);//煞車腳位(高電位放煞車低電位煞車) BRK
    digitalWrite(ST, HIGH); //停    
    pulse=0;
    Correction=true;
    sports(0);
  }
  if(Correction&&pulse<=-10){
    Correction=false;
    digitalWrite(BR, LOW);//煞車腳位(高電位放煞車低電位煞車) BRK
    digitalWrite(ST, HIGH); //停 
  }
  if (direction){
    pulse++;
   }else{
    pulse--;     
   }
  if(pulse<=UpperLimit){
    digitalWrite(BR, LOW);
    digitalWrite(ST, HIGH); //啟動    
    direction=!direction;//控制編碼器方向反轉（向下）
  }
}


void sports(bool FRsetUp){
  direction=FRsetUp;//將編碼器方向與馬達轉向同步
  digitalWrite(FR, FRsetUp); //馬達正轉
  digitalWrite(BR, LOW); //電子煞車
  digitalWrite(ST, LOW); //啟動
  analogWrite (Sp, sped); //設定轉速
}
//########################END###############################


void receiveEvent(int bytes) {
  //讀取第一個字節以確定涉及哪個寄存器
  opcode = Wire.read();
  // Serial.println(opcode);
  // 如果超過 1 個字節，則主機正在寫入從機
  if (bytes > 1) {
    if (opcode == 0x02) {
      speed = Wire.read();
      Serial.println(speed);
      Serial.println(opcode);
      sports(1);
    } else if (opcode == 0x01) {
      // speed = (Wire.read() == 1) ? 200 /* on */ : 0 /* off */;
      sports(0);
    }else if (opcode==0x03){//設定最高點位置
      SetUpperLimit(Wire.read());
    }else if (opcode==0x04){
      SetSped(Wire.read());
    }
    else if (opcode==0x05){
      EEPROM.write(0xA1,turn(UpperLimit));//寫入永久記憶體最高點位置
      EEPROM.write(0xA2,sped);//寫入永久記憶體轉速
      Serial.print("EEPROM_write");
    }
  }
}
void requestEvent() {
  // 從寄存器變量中讀取以了解要發回的內容
  Serial.print("\nEvent");
  // if (opcode == 0x02) {
  //   Wire.write((uint8_t *)&speed, sizeof(speed));
  // } else {
  //   delay(5000);
  //   // Wire.write(3);
  // }
}



  

