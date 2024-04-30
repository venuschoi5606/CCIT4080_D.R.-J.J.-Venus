#include <SoftwareSerial.h>
#include <Servo.h>

#define SOFTSERIAL_RX_PIN  2
#define SOFTSERIAL_TX_PIN  3

SoftwareSerial softSerial(SOFTSERIAL_RX_PIN,SOFTSERIAL_TX_PIN);

int ledG = 13;
int ledY = 12; 
int pinM = 11;
int inPin = 7;

Servo myservo;

int val = LOW;      // variable to store the read value

const char *voiceBuffer[] =
{
    "Turn on the light",
    "Turn off the light",

    "Play music",
    "Pause",
    "Next",
    "Previous",
    "Up",
    "Down",
    "Turn on the TV",
    "Turn off the TV",
    "Increase temperature",
    "Decrease temperature",
    "What's the time",
    "Open the door",
    "Close the door",
    "Left",

    "Right",
    "Stop",
    "Start",
    "Mode 1",
    "Mode 2",
    "Go",
};

void setup()
{
    Serial.begin(9600);
    softSerial.begin(9600);
    softSerial.listen();
    pinMode(ledG,OUTPUT);
    pinMode(ledY,OUTPUT);
    pinMode(inPin,INPUT);
    myservo.attach(11);
    digitalWrite(ledG,LOW);
    digitalWrite(ledY,LOW);
    myservo.write(0);
}

void loop()
{
    char cmd;
    val = digitalRead(inPin);
    while(val==LOW){
      digitalWrite(ledY,LOW);
      delay(500);
      val = digitalRead(inPin);
    }
    digitalWrite(ledY,HIGH);
    if(softSerial.available())
    {
        cmd = softSerial.read();
        Serial.println(voiceBuffer[cmd - 1]);
    
        if ((voiceBuffer[cmd - 1]) == "Open the door"){
          digitalWrite(ledG,HIGH);
          myservo.write(180);
          delay(3000);
          myservo.write(0);
          digitalWrite(ledG,LOW);
        }
    }
}

