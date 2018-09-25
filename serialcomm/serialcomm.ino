
byte buttonPin[12] = {0,1,2,3,4,5,6,7,8,9,10,11};//initialize I/O ports


void setup() {
  Serial.begin(9600);//setup serial communication
  for (byte i = 0;i < 12;i++){
    pinMode(buttonPin[i], INPUT_PULLUP);
  }// setup button pins
}

void loop() {
  
 int handsOnStatus = handsOnTest();// read the analysis result
 Serial.print(handsOnStatus);//output the hands_on status from 0 - 12
 Serial.println("");
   delay(40);// define the fresh rate at 25Hz
}

//handsOn analysis
int handsOnTest(){
  byte buttonValue[12] = {0,1,2,3,4,5,6,7,8,9,10,11};
  int handsOnLevel=0;
   for (byte i = 0;i < 12;i++){
       buttonValue[i] = 1 - digitalRead(buttonPin[i]);
       handsOnLevel += buttonValue[i];  
         
  }
  return handsOnLevel;
}
