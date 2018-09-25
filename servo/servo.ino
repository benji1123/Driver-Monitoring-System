#include <Servo.h>

const int MAX_LEFT  = 150;
const int MAX_RIGHT = 0;
const int STEP_SIZE = 5; // step size in degrees

const char MOVE_LEFT  = 'l';
const char MOVE_RIGHT = 'r';

Servo servo_1;
int servo_1_pin = 9;
int position = 0;

int left_led  = 12;
int right_led = 13;
int servo_led = 2;

void setup()
{
  // attach the servo to the pin 9
  servo_1.attach(servo_1_pin);

  // attach LEDs
  pinMode(left_led, OUTPUT);
  pinMode(right_led, OUTPUT);
  pinMode(servo_led, OUTPUT);

  digitalWrite(servo_led, HIGH);

  // begin serial communications
  Serial.begin(9600);
  Serial.write("Begun communications");

  // initialize servo position
//  servo_1.write(0);
  return_to_start();
}

void loop()
{
  if(Serial.available() > 0)
  {
    char input = Serial.read();
    switch(input)
    {
    // go left
    case MOVE_LEFT:      
      Serial.println("received left");
      if(position <= MAX_LEFT)
      {
        Serial.println("moving left");
        digitalWrite(left_led, HIGH);
        position += STEP_SIZE;
        delay(200);
        digitalWrite(left_led, LOW);
      }
      break;
      
    // go right
    case MOVE_RIGHT:
      Serial.println("received right");
      if(position >= MAX_RIGHT)
      {
        Serial.println("moving right");
        digitalWrite(right_led, HIGH);
        position -= STEP_SIZE;
        delay(200);
        digitalWrite(right_led, LOW);
      }
      break;
      
    default:
      break;
    }

//    Serial.println("Current position: " + position);
    servo_1.write(position);
  }
}

void return_to_start()
{
  position = 90;
  servo_1.write(position);
}
