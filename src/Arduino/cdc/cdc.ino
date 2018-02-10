// CD Changer Interface for Audi Gamma CC Bose
// by Orlin Tomov <mail:oritomov@yahoo.com>

// Receives data from HU as an I2C/TWI slave device and send it via UART to CDC.
// Receines data from CDC via UART and send it to HU via custom Gamma protocol

// Created 5 Jun 2016

// This code is in the public domain.

#include <Wire.h>
#include "gamma.h"
#include "vag.h"

// the pin that the LED is attached to
#define ledPin            13
// the pin that will off SDA ground
#define readyPin          12

// i2c address
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
// probably instead of 'stop'
#define HU_NO_IDEA        (uint16_t)0x9212
// or
#define HU_CANCEL         (uint16_t)0x22A2

#define HU_LEFT_RIGHT     (uint16_t)0x0102
#define HU_RIGHT_LEFT     (uint16_t)0x0201

#define HU_STATUS         (uint8_t)0x34

// NOTE! Those are two made up commands in order to change the CDs
#define CDC_NEXT_CD       (uint8_t)0xFE
#define CDC_PREV_CD       (uint8_t)0xFF

#define CDC_NO_DISK       (uint8_t)0x20

#define HU_STATUS_HEAD    (uint8_t)0
#define HU_STATUS_CD      (uint8_t)1
#define HU_STATUS_TR      (uint8_t)2

int hu_handshaked;
int started;
uint32_t previousMillis;
uint16_t cdc_command;
uint8_t cdc_cd;
uint8_t cdc_tr;

void setup() {
  hu_handshaked = false;
  started = false;
  cdc_command = 0;
  cdc_cd = 1;
  cdc_tr = 1;

  // setting off SDA ground after boot
  pinMode(readyPin, OUTPUT);
  digitalWrite(readyPin, HIGH);

  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);     // turn on the LED:

  Serial.begin(9600);             // start serial for output, SERIAL_8N1 data, parity, and stop bits

  wire();                         // join i2c bus

  digitalWrite(ledPin, LOW);      // turn off the LED:
}

void loop() {
  if (cdc_command != 0) {
    // start
    if (cdc_command == HU_START) {
      started = true;
      cdc_command = 0;
    }
    // stop
    if (cdc_command == HU_STOP) {
      started = false;
      hu_handshaked = false;
      cdc_command = 0;
    }
  }
 
  if (started) {
    // handshake. means read and write status if any
    if (not hu_handshaked) {
      hu_handshake();
    }

    // write status
    if (cdc_status()) {
      gamma();
    }
  }
  delay(1);
}

void wire() {
  Wire.begin(HU_I2C_ADDRESS);     // join i2c bus with address #40
  Wire.onReceive(receiveEvent);   // register event
}

void hu_handshake() {
  // when started but not handshaked
  if (cdc_status()) {
    gamma();
  } else {
    // wait for a while
    //delay(3000);
    uint32_t currentMillis = millis();
    if (currentMillis - previousMillis >= 3000) {
      previousMillis = currentMillis;
      // trying again
      digitalWrite(ledPin, HIGH);
      Serial.write(CDC_PLAY);
      Serial.write(CDC_END_CMD);
      digitalWrite(ledPin, LOW);
    }
  }
}

// check for status from the CDC
int cdc_status() {
  static uint8_t status = HU_STATUS_HEAD;
  if (Serial.available() > 0) {
    hu_handshaked = true;
    digitalWrite(ledPin, HIGH);     // turn on the LED:
    // read the incoming byte:
    uint8_t incomingByte = Serial.read();
    switch (status) {
      case HU_STATUS_HEAD:
        if (incomingByte == HU_STATUS) {
          status = HU_STATUS_CD;
        } else {
          Serial.println(incomingByte, HEX);
        }
        break;
      case HU_STATUS_CD:
        cdc_cd = incomingByte;
        status = HU_STATUS_TR;
        break;
      case HU_STATUS_TR:
        cdc_tr = incomingByte;
        status = HU_STATUS_HEAD;
        digitalWrite(ledPin, LOW);      // turn off the LED:
        //char s[100];
        //sprintf(s, "%x %x %x", incomingByte, cdc_cd, cdc_tr);
        //Serial.println(s);
        return true;
      default:
        status = HU_STATUS_HEAD;
        Serial.println(incomingByte, HEX);
    }
    digitalWrite(ledPin, LOW);      // turn off the LED:
  }
  return false;
}

void prepare(uint8_t* data) {
  data[0] = cdc_cd;
  data[1] = cdc_tr;
  uint16_t check = cdc_cd + cdc_tr + 1;
  if ((check & 0x1F0) && ((check - (cdc_cd & 0x0f)) <= (check & 0x1F0))) {
    check -= 0x10;
  }
  data[2] = check;
}

// uses custom Gamma protocol to report CDC status
void gamma() {
  Wire.end();                     // stops I2C bus
  delay(30);
  digitalWrite(ledPin, HIGH);     // turn on the LED:
  uint8_t data[3];
  prepare(data);
  Gamma.transmit(HU_I2C_ADDRESS, data);
  digitalWrite(ledPin, LOW);      // turn off the LED:
  wire();                         // restart I2C buss
}

// function that executes whenever data is received from I2C master
// this function is registered as an event, see setup()
// translate command for the CDC
void receiveEvent(int howMany) {
  digitalWrite(ledPin, HIGH);     // turn on the LED:
  while (0 < Wire.available()) {  // loop through all but the last
    uint8_t x0 = Wire.read();         // receive byte as a character
    if (0 < Wire.available()) {
      uint8_t x1 = Wire.read();       // receive byte as an integer
      uint16_t x = ((x1 << 8) + x0);
      switch (x) {
        case HU_START:
          Serial.write(CDC_PLAY);
          Serial.write(CDC_END_CMD);
          // response
          cdc_command = HU_START;
          previousMillis = millis();
          break;
        case HU_STOP:
          Serial.write(CDC_STOP);
          Serial.write(CDC_END_CMD);
          cdc_command = HU_STOP;
          break;
        case HU_LEFT_HOLD:
          cdc_command = HU_LEFT_HOLD;
          break;
        case HU_LEFT_RELEASE:
          if (cdc_command == HU_LEFT_HOLD) {
            Serial.write(CDC_PREV);
          } else {
            Serial.write(CDC_SHFFL);
          }
          cdc_command = 0;
          break;
        case HU_RIGHT_HOLD:
          cdc_command = HU_RIGHT_HOLD;
          break;
        case HU_RIGHT_RELEASE:
          if (cdc_command == HU_RIGHT_HOLD) {
            Serial.write(CDC_NEXT);
          } else {
            Serial.write(CDC_SEQNT);
          }
          cdc_command = 0;
          break;
        case HU_DOWN_HOLD:
          break;
        case HU_DOWN_RELEASE:
          Serial.write(CDC_NEXT_CD);
          break;
        case HU_UP_HOLD:
          break;
        case HU_UP_RELEASE:
          Serial.write(CDC_PREV_CD);
          break;
        case HU_NO_IDEA:
          Serial.print("no idea "); //unknow
          Serial.println(HU_NO_IDEA);
          break;
        case HU_CANCEL:
          Serial.print("cancel "); //unknow
          Serial.println(HU_CANCEL);
          break;
        default:
          Serial.print("??"); //unknow
          Serial.println(x, HEX); // print the integer
      }
    } else {
      Serial.print("?"); //unknow
      Serial.println(x0, HEX);    // print the integer
    }
  }
  digitalWrite(ledPin, LOW);      // turn off the LED:
}

