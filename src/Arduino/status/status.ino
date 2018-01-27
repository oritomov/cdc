#include <Wire.h>
#include "gamma.h"

// the pin that will off SDA ground
#define readyPin          12

// HU i2c address
#define HU_I2C_ADDRESS    (uint8_t)0x40

// Commands from HU via i2c
#define HU_START          (uint16_t)0x21A1
#define HU_STOP           (uint16_t)0xA121
#define HU_LEFT_HOLD      (uint16_t)0x0181
#define HU_LEFT_RELEASE   (uint16_t)0x8101
#define HU_RIGHT_HOLD     (uint16_t)0x0282
#define HU_RIGHT_RELEASE  (uint16_t)0x8202
#define HU_DOWN_HOLD      (uint16_t)0x0383
#define HU_DOWN_RELEASE   (uint16_t)0x8303
#define HU_UP_HOLD        (uint16_t)0x0484
#define HU_UP_RELEASE     (uint16_t)0x8404

uint16_t cdc_command;
uint8_t cd, tr;

void setup() {
//  Serial.begin(9600);             // start serial for output, SERIAL_8N1 data, parity, and stop bits

  // setting off SDA ground after boot
  pinMode(readyPin, OUTPUT);
  digitalWrite(readyPin, HIGH);

  wire();

  cdc_command = 0;
  cd = 0;
  tr = 0;
//  Serial.println("ready!");
}

void loop() {
  if (cdc_command > 0) {
    switch(cdc_command){
      case HU_START:
        break;
      case HU_RIGHT_RELEASE:
        tr++;
        break;
      case HU_LEFT_RELEASE:
        tr--;
        break;
      case HU_DOWN_RELEASE:
        cd++;
        break;
      case HU_UP_RELEASE:
        cd--;
        break;
    }
    Wire.end();
    gamma();
    wire();
  }
}

void wire() {
  Wire.begin(HU_I2C_ADDRESS);     // join i2c bus with address #40
  Wire.onReceive(receiveEvent);   // register event
}

void prepare(uint8_t* data) {
  data[0] = cd;
  data[1] = tr;
  data[2] = cd+tr+1;
}

void gamma() {
  delay(30);
  uint8_t data[3];
  prepare(data);
  Gamma.transmit(HU_I2C_ADDRESS, data);
  char s[100];
  sprintf(s, "at: 0x%x - %d, %d, %d", HU_I2C_ADDRESS, data[0], data[1], data[2]);
  Serial.println(s);
  cdc_command = 0;
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  while (0 < Wire.available()) {  // loop through all but the last
    uint8_t x0 = Wire.read();         // receive byte as a character
    if (0 < Wire.available()) {
      uint8_t x1 = Wire.read();       // receive byte as an integer
      uint16_t x = ((x1 << 8) + x0);
      switch (x) {
        case HU_START:
          Serial.println("START");
          cdc_command = HU_START;
          break;
        case HU_STOP:
          Serial.println("HU_STOP");
          cdc_command = 0;
          break;
        case HU_RIGHT_HOLD:
          Serial.println("HU_RIGHT_HOLD");
//          command = HU_RIGHT_HOLD;
          break;
        case HU_RIGHT_RELEASE:
          Serial.println("HU_RIGHT_RELEASE");
          cdc_command = HU_RIGHT_RELEASE;
          break;
        case HU_LEFT_HOLD:
          Serial.println("HU_LEFT_HOLD");
//          command = HU_LEFT_HOLD;
          break;
        case HU_LEFT_RELEASE:
          Serial.println("HU_LEFT_RELEASE");
          cdc_command = HU_LEFT_RELEASE;
          break;
        case HU_UP_HOLD:
          Serial.println("HU_UP_HOLD");
//          command = HU_UP_HOLD;
          break;
        case HU_UP_RELEASE:
          Serial.println("HU_UP_RELEASE");
          cdc_command = HU_UP_RELEASE;
          break;
        case HU_DOWN_HOLD:
          Serial.println("HU_DOWN_HOLD");
//          command = HU_DOWN_HOLD;
          break;
        case HU_DOWN_RELEASE:
          Serial.println("HU_DOWN_RELEASE");
          cdc_command = HU_DOWN_RELEASE;
          break;
        default:
          Serial.print("??"); //unknow
          Serial.println(x, HEX); // print the integer
      } //switch
    } else {
      Serial.print("?"); //unknow
      Serial.println(x0, HEX);    // print the integer
    }  //if wire
  } //wile wire
} // end of receiveEvent

