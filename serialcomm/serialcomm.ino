/*12 buttons version
 * output a distraction level according to driver's hands_on status
 * updated on Tue 5:18AM by Jarvis
 */
byte buttonPin[12] = {0,1,2,3,4,5,6,7,8,9,10,11};//initialize I/O ports


void setup() {
    Serial.begin(9600);//setup serial communication
    for (byte i = 0;i < 12;i++){
    pinMode(buttonPin[i], INPUT_PULLUP);
  }// setup button pins
}

void loop() {
  
   int distractionStatus = handsOnTest();// read the analysis result
   Serial.println(distractionStatus);//output the distraction status from 0 - 2
   delay(40);// define the fresh rate at 25Hz
}

//handsOn analysis
int handsOnTest(){
   byte buttonValue[12] = {0,1,2,3,4,5,6,7,8,9,10,11};
   int handsOnLevel = 0;// # of buttons detect driver's hands_on
   int wheel_score = 0;// level of driver's distraction, higher is safer
   for (byte i = 0;i < 12;i++){
       buttonValue[i] = 1 - digitalRead(buttonPin[i]);
       handsOnLevel += buttonValue[i];  
  }
  switch(handsOnLevel){
    case 0:
    case 1:
    case 2:
      wheel_score = 0;//distraction
      break;
      
    case 3:
    case 4:
    case 5:
      wheel_score = 1;//normal focus
      break;
      
    case 6:
    case 7:
    case 8:
    case 9:
    case 10:
    case 11:
    case 12:
      wheel_score = 2;//both hands on
      break; 
  }
  return wheel_score;
}
