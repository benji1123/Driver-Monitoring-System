/*8 buttons version
 * output a distraction level through LED according to driver's hands_on status
 * updated on Wed 4:20PM by Jarvis
 */
byte buttonPin[8]= {1,2,3,4,5,6,7};//initialize I/O ports
byte ledPin[3]={9,10,11};//initialize I/O ports
int dp = 0;//counter
int handsOnTest(void);
void alarm(int color);
void setup() {
    Serial.begin(9600);//setup serial communication
    for (byte i = 0;i < 8;i++){
    pinMode(buttonPin[i], INPUT_PULLUP);
     }
    //pinMode(13,OUTPUT);//onboard LED
    for(byte i = 9;i < 12;i++){
    pinMode(ledPin[i], OUTPUT);//LED alarm
    }
 // setup button pins
}

void loop() {
  
    int wheel_score = handsOnTest();// read the analysis result
    
    //detect if the driver's hands are not on the wheel for a while
    if(wheel_score < 2) dp++;
    else dp = 0;
    if(dp>100&&dp<=300) alarm(wheel_score);  // hands not on wheel over 4 seconds
    
    else if(dp>300) dp=0;//clear the cache
    else alarm(2);
   
    //receive eyetracking result
    /*if(Serial.available()>0){
      if(Serial.read() == 2) alarm(2);
    */  
    
    
    Serial.println(wheel_score);//output the distraction status from 0 - 2
    delay(40);// define the fresh rate at 25Hz
}

//handsOn analysis
int handsOnTest(){
   byte buttonValue[8] = {0,1,2,3,4,5,6,7};
   int handsOnLevel = 0;// # of buttons detect driver's hands_on
   int wheel_score = 0;// level of driver's distraction, higher is safer
   for (byte i = 0;i < 8;i++){
       buttonValue[i] = 1 - digitalRead(buttonPin[i]);
       handsOnLevel += buttonValue[i];  
  }
  switch(handsOnLevel){
    case 0:
      wheel_score = 0;//distraction
      break;
    case 1: 
      wheel_score = 1;//normal focus
      break;
    case 2:  
    case 3:
    case 4:
    case 5:  
    case 6:
    case 7:
      wheel_score = 2;//both hands on
      break; 
  }
  
  return wheel_score;
}

void alarm(int color){
  int color_pin = 20;
  switch(color){
    case 0:
      color_pin = 9;//distraction, red
      break;
    case 1:
      color_pin = 10;//moderate, yellow
      break; 
    case 2: 
      color_pin = 11;//both hands on, green
      break;
  }

  if(color<2){
  digitalWrite(ledPin[color_pin], HIGH);
  delay(150);
  digitalWrite(ledPin[color_pin], LOW);
  delay(150);
  digitalWrite(ledPin[color_pin], HIGH);
  delay(150);
  digitalWrite(ledPin[color_pin], LOW);
  delay(150);
  }
  else digitalWrite(ledPin[color_pin], HIGH);
}
