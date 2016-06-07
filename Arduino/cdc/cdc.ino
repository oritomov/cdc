// CD Changer Interface for Audi Gamma CC Bose
// by Orlin Tomov <mail:oritomov@yahoo.com>

// Receives data as an I2C/TWI slave device

// Created 5 Jun 2016

// This code is in the public domain.


#include <Wire.h>

const int ledPin = 13; // the pin that the LED is attached to

const unsigned int cdc_on            = 0x21A1;
const unsigned int cdc_off           = 0xA121;
const unsigned int cdc_left_hold     = 0x0181;
const unsigned int cdc_left_release  = 0x8101;
const unsigned int cdc_right_hold    = 0x0282;
const unsigned int cdc_right_release = 0x8202;
const unsigned int cdc_down_hold     = 0x0383;
const unsigned int cdc_down_release  = 0x8303;
const unsigned int cdc_up_hold       = 0x0484;
const unsigned int cdc_up_release    = 0x8404;
int cdc_command;

void setup() {
  cdc_command = 0;
  // initialize the LED pin as an output:
  /**/pinMode(ledPin, OUTPUT);

  Wire.begin(64);                 // join i2c bus with address #40

  // set baud rite 960
  TWBR = 130;                     // ((16 MHz / 960 Hz) - 16) / 2 / 64
  //Serial.println(TWBR, HEX);
  /* Select 64 as the prescaler value - see page 239 of the data sheet */
  /**/TWSR |= bit (TWPS1);
  /**/TWSR |= bit (TWPS0);
  //Serial.println(TWSR, HEX);
 
  Wire.onRequest(requestEvent);   // interrupt handler for when data is wanted
  
  Wire.onReceive(receiveEvent);   // register event

  Serial.begin(9600);             // start serial for output
}

void loop() {
  delay(100);
  //check();
}

void check() {
  if (cdc_command != 0) {
    digitalWrite(ledPin, HIGH);   // turn on the LED:
    for (int j = 0; j < 5; j++) {
      delay(100);

      byte count = 0;
      for (byte i = 8; i < 120; i++)
      {
        Wire.beginTransmission (i);
        if (Wire.endTransmission () == 0)
        {
          Serial.print ("Found address: ");
          Serial.print (i, DEC);
          Serial.print (" (0x");
          Serial.print (i, HEX);
          Serial.println (")");
          count++;
          //delay (1);            // maybe unneeded?
        } // end of good response
      } // end of for loop
      //Serial.println ("Done.");
      //Serial.print ("Found ");
      //Serial.print (count, DEC);
      //Serial.println (" device(s).");
    }
    Serial.println ("Done.");
    cdc_command = 0;
    digitalWrite(ledPin, LOW);    // turn off the LED:
  }
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {

  while (0 < Wire.available()) {  // loop through all but the last
    int x0 = Wire.read();         // receive byte as a character
    if (0 < Wire.available()) {
      int x1 = Wire.read();       // receive byte as an integer
      unsigned int x = ((x1 << 8) + x0);
      switch (x) {
        case cdc_on:
          Serial.println("ON");
          cdc_command = cdc_on;
          // TODO: answer
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
          Serial.println(x, HEX); // print the integer
      }
    } else {
      Serial.println(x0, HEX);      // print the integer
    }
  }
}

// called by interrupt service routine when response is wanted
void requestEvent () {
  Serial.println("!!!!!!");
  digitalWrite(ledPin, HIGH);     // turn on the LED:
  Wire.write (0xFF);              // send response
} // end of requestEvent
