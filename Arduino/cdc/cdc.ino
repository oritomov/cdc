// CD Changer Interface for Audi Gamma CC Bose
// by Orlin Tomov <mail:oritomov@yahoo.com>

// Receives data as an I2C/TWI slave device

// Created 5 Jun 2016

// This code is in the public domain.


#include <Wire.h>

const int ledPin = 13; // the pin that the LED is attached to

const int cdc_on            = 0x21;
const int cdc_off           = 0xA1;
const int cdc_left_hold     = 0x01;
const int cdc_left_release  = 0x81;
const int cdc_right_hold    = 0x02;
const int cdc_right_release = 0x82;
const int cdc_down_hold     = 0x03;
const int cdc_down_release  = 0x83;
const int cdc_up_hold       = 0x04;
const int cdc_up_release    = 0x84;
int cdc_command;

void setup() {
  cdc_command = 0;
  // initialize the LED pin as an output:
  /**/pinMode(ledPin, OUTPUT);

  Wire.begin(64);               // join i2c bus with address #8
  //Wire.setClock(9600);        // set baud rite
 
  //digitalWrite(ledPin, HIGH); // turn on the LED:

  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void loop() {
  delay(100);
  if (cdc_command != 0) {
    digitalWrite(ledPin, HIGH); // turn on the LED:
    //for (int j = 0; j < 20; j++) {
      delay(100);

      byte count = 0;
      for (byte i = 8; i < 120; i++)
      {
        // set baud rite 9600
        /**/TWBR = 130;  // 1 kHz 
         /* Select 4 as the prescaler value - see page 239 of the data sheet */
       /**/TWSR |= bit (TWPS1);  //&= ~cbi change prescaler 4
        /**/TWSR |= bit (TWPS0);  //|=sbi change prescaler 4
        
        Wire.beginTransmission (i);
        //Serial.println(TWBR, HEX);
        //Serial.println(TWSR, HEX);
        if (Wire.endTransmission () == 0)
        {
          Serial.print ("Found address: ");
          Serial.print (i, DEC);
          Serial.print (" (0x");
          Serial.print (i, HEX);
          Serial.println (")");
          count++;
          delay (1);  // maybe unneeded?
        } // end of good response
      } // end of for loop
      Serial.println ("Done.");
      Serial.print ("Found ");
      Serial.print (count, DEC);
      Serial.println (" device(s).");
    }
  //}
  cdc_command = 0;
  digitalWrite(ledPin, LOW); // if it's an L (ASCII 76) turn off the LED:
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {

  //digitalWrite(ledPin, LOW); // if it's an L (ASCII 76) turn off the LED:

  while (1 < Wire.available()) {  // loop through all but the last
        Serial.println(TWBR, HEX);
        Serial.println(TWSR, HEX);
    int y = Wire.read();         // receive byte as a character
    Serial.print(y, HEX);            // print the character
    Serial.print(" ");            // print the character
    int x = Wire.read();          // receive byte as an integer
    switch (x) {
      case cdc_on:
        Serial.println("ON");
        cdc_command = cdc_on;
// TODO: answer
//        Wire.write(byte(0x34));
//        Wire.write(byte(0xBE));
//        Wire.write(byte(0xFF));
//        Wire.write(byte(0xFF));
//        Wire.write(byte(0xFF));
//        Wire.write(byte(0xFF));
//        Wire.write(byte(0xCF));
//        Wire.write(byte(0x3C));
        break;
      case cdc_off:
        Serial.println("OFF");
        break;
      case cdc_left_hold:
        Serial.println("LEFT HOLD");
        break;
      case cdc_left_release:
        Serial.println("LEFT RELEASE");
        break;
      case cdc_right_hold:
        Serial.println("RIGHT HOLD");
        break;
      case cdc_right_release:
        Serial.println("RIGHT RELEASE");
        break;
      case cdc_down_hold:
        Serial.println("DOWN HOLD");
        break;
      case cdc_down_release:
        Serial.println("DOWN RELEASE");
        break;
      case cdc_up_hold:
        Serial.println("UP HOLD");
        break;
      case cdc_up_release:
        Serial.println("UP RELEASE");
        break;
      default:
        Serial.println(x);        // print the integer
    }
  }
}
