#include "gamma.h"

    Gamma::Gamma() {
      job = I2C_DO_NOTHING;
      step = 0;
      address = 0;
      index = 0;
      pinMode(I2C_SDA, OUTPUT);
      pinMode(I2C_SCL, OUTPUT);
    }

    void Gamma::SDA(int turn) {
      if (turn) {
        digitalWrite(I2C_SDA, HIGH);
      } else {
        digitalWrite(I2C_SDA, LOW);
      }
    }

    void Gamma::SCL(int turn) {
      if (turn) {
        digitalWrite(I2C_SCL, HIGH);
      } else {
        digitalWrite(I2C_SCL, LOW);
      }
    }

    void Gamma::transmit(uint8_t address, uint8_t* data) {
      this->address = address;
      for (int i = 0; i < I2C_DATA_LEN; i++) {
        this->data[i] = data[i];
      }
      job = I2C_START;
      step = 0;
      index = 0;

      // initialize timer1 
      noInterrupts();           // disable all interrupts

      TCCR1A = 0;
      TCCR1B = 0;
      TCNT1  = 0;

      OCR1A = 8333;             // compare match register 16MHz/1/960Hz * 2
                                // it is ok between 0x200 & 0x2300
      TCCR1B |= (1 << WGM12);   // CTC mode
      TCCR1B |= (1 << CS10);    // 1 prescaler 
      TIMSK1 |= (1 << OCIE1A);  // enable timer compare interrupt

      interrupts();             // enable all interrupts
      
      delay(40);                // Note! do nothing but transmit
    }

    void Gamma::work(void) {
      static uint8_t datum;
      switch (job) {
        case I2C_DO_NOTHING:
          return;

        case I2C_START:
          switch (step) {
            case 0:
              SDA(1);            // i2c start bit sequence
              SCL(1);
              break;
            case 1:
              SDA(0);
              step = I2C_FINAL;
              break;
          }
          break;

        case I2C_STOP:
          switch (step) {
            case 0:
              SDA(0);            // i2c stop bit sequence
              SCL(0);
              break;
            case 1:
              SCL(1);
              break;
            case 2:
              SDA(1);
              step = I2C_FINAL;
              job = I2C_FINAL;
              break;
          }
          break;

        case I2C_ADDRESS:
          if (step == 0) {
            datum = address << 1;    // I2C address with R/W bit
          }
          if (step % 2 == 0) {            // even step
            if(datum & 0x80) {
              SDA(1);
            } else if (step == 16) {
              SDA(1);            // acknowledge bit
            } else {
              SDA(0);
            }
            SCL(0);
            datum <<= 1;
          } else {                    // odd step
            SCL(1);
          }
          if (step == I2C_LAST_DATA_BIT) {
            step = I2C_FINAL;
          }
          break;

        case I2C_DATA:
          if (step % 2 == 0) {            // even step
            if (step == 0) {
              datum = data[index];
              SDA(0);
              SCL(0);
              // do nothing
              break;
            }
            if(datum & 0x80) {
              SDA(1);
            } else {
              SDA(0);
            }
            if (step > 0) {
              datum <<= 1;
            }
            SCL(0);
          } else {                    // odd step
            SCL(1);
          }
          if (step == I2C_LAST_DATA_BIT) {
            index++;
            if (index < I2C_DATA_LEN) {
              job--;    // continue to send data
            }
            step = I2C_FINAL;
          }
          break;
        }
        if (step == I2C_FINAL) {
            job++;
        }
        step++;
      }

// Interrupt is called depend of frequency 
ISR(TIMER1_COMPA_vect) {
  Gamma.work();
}

