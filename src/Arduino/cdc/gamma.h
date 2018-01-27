#ifndef gamma_h
#define gamma_h

#define I2C_SDA             18
#define I2C_SCL             19

#define I2C_DATA_LEN        3

#define I2C_DO_NOTHING      0
#define I2C_START           1
#define I2C_ADDRESS         2
#define I2C_DATA            3
#define I2C_STOP            4
#define I2C_LAST_DATA_BIT   17
#define I2C_FINAL           0xFF

class Gamma {
  //privare:
    uint8_t address;
    uint8_t data[I2C_DATA_LEN];
    uint32_t index;
    uint8_t job;
    uint8_t step;


    void SDA(int);
    void SCL(int);

  public:
    Gamma();
    void transmit(uint8_t address, uint8_t* data);
    void work(void);
} Gamma;

#endif
