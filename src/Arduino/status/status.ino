#include "my_wire.h"

// HU i2c address
const byte HU_I2C_ADDRESS           = 0x40;

// Commands from HU via i2c
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

unsigned int command;
byte cd, tr;

void setup() {
  Serial.begin(9600);             // start serial for output, SERIAL_8N1 data, parity, and stop bits

  MyWire.begin(HU_I2C_ADDRESS);     // join i2c bus with address #40
  MyWire.onReceive(receiveEvent);   // register event

  // set baud rite 960
  TWBR = 130;                     // ((16 MHz / 960 Hz) - 16) / 2 / 64

  //Serial.println(TWBR, HEX);
  /* Select 64 as the prescaler value - see page 239 of the data sheet */
  TWSR |= bit (TWPS1);
  TWSR |= bit (TWPS0);
  //Serial.println(TWSR, HEX);

  command = 0;
  cd = 0;
  tr = 0;
  Serial.println("ready!");
}

void loop() {
  if (command > 0) {
    byte n;
    switch(command){
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
    n = 1;
    write(n);
  }
}

void prepare(byte* data) {
  //no cd     16, x, x
  data[0] = cd;
  data[1] = tr;
  data[2] = cd+tr+1;
}

void write(byte n) {
  byte data[3];
  prepare(data);
  for (int i = 0; i < n; i++) {
    MyWire.beginTransmission(HU_I2C_ADDRESS);
    size_t size = MyWire.write(data, sizeof(data));
    byte res = MyWire.endTransmission();
    char s[100];
    sprintf(s, "at: 0x%x - %d, %d, %d", HU_I2C_ADDRESS, data[0], data[1], data[2]);
    Serial.println(s);
    if (res != 0) {
      Serial.print(res);
      Serial.println(" twi error!");
      break;
    }
    if (i < n - 1) {
      delay(30);
    }
  }
  command = 0;
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  while (0 < MyWire.available()) {  // loop through all but the last
    int x0 = MyWire.read();         // receive byte as a character
    if (0 < MyWire.available()) {
      int x1 = MyWire.read();       // receive byte as an integer
      unsigned int x = ((x1 << 8) + x0);
      switch (x) {
        case HU_START:
          Serial.println("START");
          command = HU_START;
          break;
        case HU_STOP:
          Serial.println("HU_STOP");
          command = 0;
          break;
        case HU_RIGHT_HOLD:
          Serial.println("HU_RIGHT_HOLD");
//          command = HU_RIGHT_HOLD;
          break;
        case HU_RIGHT_RELEASE:
          Serial.println("HU_RIGHT_RELEASE");
          command = HU_RIGHT_RELEASE;
          break;
        case HU_LEFT_HOLD:
          Serial.println("HU_LEFT_HOLD");
//          command = HU_LEFT_HOLD;
          break;
        case HU_LEFT_RELEASE:
          Serial.println("HU_LEFT_RELEASE");
          command = HU_LEFT_RELEASE;
          break;
        case HU_UP_HOLD:
          Serial.println("HU_UP_HOLD");
//          command = HU_UP_HOLD;
          break;
        case HU_UP_RELEASE:
          Serial.println("HU_UP_RELEASE");
          command = HU_UP_RELEASE;
          break;
        case HU_DOWN_HOLD:
          Serial.println("HU_DOWN_HOLD");
//          command = HU_DOWN_HOLD;
          break;
        case HU_DOWN_RELEASE:
          Serial.println("HU_DOWN_RELEASE");
          command = HU_DOWN_RELEASE;
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

