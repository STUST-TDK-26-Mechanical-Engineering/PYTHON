#define DO1 5
#define DO2 4
#define DO3 3
#define DO4 2
#define RDO1 6  
#define RDO2 7
#define RDO3 8
#define RDO4 9
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
}

void loop() {
  Serial.print(digitalRead(DO1));
  Serial.print("\t");
  Serial.print(digitalRead(DO2));
  Serial.print("\t");
  Serial.print(digitalRead(DO3));
  Serial.print("\t");
  Serial.print(digitalRead(DO4));
  Serial.print("\t");
  Serial.print(digitalRead(RDO1));
  Serial.print("\t");
  Serial.print(digitalRead(RDO2));
  Serial.print("\t");
  Serial.print(digitalRead(RDO3));
  Serial.print("\t");
  Serial.print(digitalRead(RDO4));
  Serial.print("\n");
  // delay(500);
}
