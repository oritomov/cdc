#include <Wire.h>

// AI i2c address
const byte AI_I2C_ADDRESS           = 0x00;

// HU i2c address
const byte HU_I2C_ADDRESS           = 0x40;

// Commands from HU via i2c
const unsigned int HU_START         = 0x21A1;
const unsigned int HU_STOP          = 0xA121;
const unsigned int HU_LEFT_HOLD     = 0x0181;
const unsigned int HU_LEFT_RELEASE  = 0x8101;
const unsigned int HU_RIGHT_HOLD    = 0x0282;
const unsigned int HU_RIGHT_RELEASE = 0x8202;

unsigned int command;

void setup() {
  Serial.begin(9600);             // start serial for output, SERIAL_8N1 data, parity, and stop bits
  Serial.println("Hello");

  Wire.begin(HU_I2C_ADDRESS);     // join i2c bus with address #40

  // set baud rite 900
  TWBR = 139;                     // ((16 MHz / 900 Hz) - 16) / 2 / 64
  // almost there - it is set to 898.4725966
  //Serial.println(TWBR, HEX);
  /* Select 64 as the prescaler value - see page 239 of the data sheet */
  TWSR |= bit (TWPS1);
  TWSR |= bit (TWPS0);
  //Serial.println(TWSR, HEX);
 
  Wire.onRequest(requestEvent);   // interrupt handler for when data is wanted

  Wire.onReceive(receiveEvent);   // register event

  command = 0;
}

void loop() {
  response();
}

void response() {
  switch (command) {
    case HU_START: 
    {
      byte value[] = {0, 1, 1, 3};
      respond(1, value, 80);
      command = 0;
      Serial.println("START");
      break;
    }
    case HU_LEFT_HOLD:
    {
      byte value[] = {0, 1, 1, 3};
      respond(1, value, 30);
      command = 0;
      Serial.println("LEFT_HOLD");
      break;
    }
    case HU_LEFT_RELEASE:
    {
      byte value[] = {0, 1, 2, 4};
      respond(2, value, 30);
      command = 0;
      Serial.println("LEFT_RELEASE");
      break;
    }
    case HU_RIGHT_HOLD:
    {
      byte value[] = {0, 0, 1, 2};
      respond(1, value, 30);
      command = 0;
      Serial.println("RIGHT_HOLD");
      break;
    }
    case HU_RIGHT_RELEASE:
    {
      byte value[] = {0, 0, 1, 2};
      respond(2, value, 30);
      command = 0;
      Serial.println("RIGHT_RELEASE");
      break;
    }
  }
}

void respond(byte n, byte value[], int ms) {
  //Serial.println("responding...");
  for (byte i = 0; i < n; i++)
  {
    delay(ms);
    Wire.beginTransmission(value[0]);
    Wire.write(value[1]);
    Wire.write(value[2]);
    Wire.write(value[3]);
    if (Wire.endTransmission() == 0)
    {
        
    }
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
      //Serial.println("START");
          command = HU_START;
          break;
        case HU_STOP:
          command = 0;
          break;
        case HU_LEFT_HOLD:
      //Serial.println("LEFT_HOLD");
          command = HU_LEFT_HOLD;
          break;
        case HU_LEFT_RELEASE:
          command = HU_LEFT_RELEASE;
          break;
        case HU_RIGHT_HOLD:
          command = HU_RIGHT_HOLD;
          break;
        case HU_RIGHT_RELEASE:
          command = HU_RIGHT_RELEASE;
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
} // end of receiveEvent

// called by interrupt service routine when response is wanted
void requestEvent () {
  Serial.println("!!!!!!");
} // end of requestEvent

