byte buttonPin[12] = {0,1,2,3,4,5,6,7,8,9,10,11};//initialize I/O ports

void setup() {
  Serial.begin(9600);//setup serial communication
  for (byte i = 0;i < 12;i++){
    pinMode(buttonPin[i], INPUT_PULLUP);
  }// setup button pins
}

void loop() {
  
 int distractionStatus = distractionTest();// read the analysis result
 Serial.print(distractionStatus);
 Serial.println("");
   delay(40);// define the fresh rate at 25Hz
}

//distraction analysis
int distractionTest(){
  byte buttonValue[3] = {5,6,7};
  int logic=0;
   for (byte i = 5;i < 8;i++){
       buttonValue[i] = 1 - digitalRead(buttonPin[i]);
       logic += buttonValue[i];  
  }
  return logic;
}
