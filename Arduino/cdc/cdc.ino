// CD Changer Interface for Audi Gamma CC Bose
// by Orlin Tomov <mail:oritomov@yahoo.com>

// Receives data as an I2C/TWI slave device

// Created 5 Jun 2016

// This code is in the public domain.


#include <Wire.h>

const int ledPin = 13; // the pin that the LED is attached to

const unsigned int HU_START         = 0x21A1;
const unsigned int HU_STOP          = 0xA121;
const unsigned int HU_LEFT_HOLD     = 0x0181;
const unsigned int HU_LEFT_RELEASE  = 0x8101;
const unsigned int HU_RIGHT_HOLD    = 0x0282;
const unsigned int HU_RIGHT_RELEASE = 0x8202;
const unsigned int HU_DOWN_HOLD     = 0x0383;
const unsigned int HU_DOWN_RELEASE  = 0x8303;
const unsigned int HU_UP_HOLD       = 0x0484;
const unsigned int HU_UP_RELEASE    = 0x8404;
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
        case HU_START:
          Serial.println("ON");
          cdc_command = 1;
          // TODO: answer
          break;
        case HU_STOP:
          Serial.println("OFF");
          break;
        case HU_LEFT_HOLD:
          Serial.println("LEFT HOLD");
          break;
        case HU_LEFT_RELEASE:
          Serial.println("LEFT RELEASE");
          break;
        case HU_RIGHT_HOLD:
          Serial.println("RIGHT HOLD");
          break;
        case HU_RIGHT_RELEASE:
          Serial.println("RIGHT RELEASE");
          break;
        case HU_DOWN_HOLD:
          Serial.println("DOWN HOLD");
          break;
        case HU_DOWN_RELEASE:
          Serial.println("DOWN RELEASE");
          break;
        case HU_UP_HOLD:
          Serial.println("UP HOLD");
          break;
        case HU_UP_RELEASE:
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
