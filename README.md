# Audi Gamma CC Bose CD Changer Emulator Arduino Raspbery Pi

### Audi Gamma CC Bose

![](https://github.com/oritomov/cdc/blob/master/Audo%20Gamma%20CC%20Bose.jpg)

### Audi Gamma CC Bose pinout

![](https://github.com/oritomov/cdc/blob/master/Audo%20Gamma%20CC%20Bose%20pinout.jpg)

### OFF

![](https://github.com/oritomov/cdc/blob/master/off.png)

 * 1000000 (7bit addrtess 0x40)
 * 0 (Write)
 * 0 (Ack)
 * 00100001 (8bit data 0x21)
 * 0 (Ack)
 * 10100001 (8bit data 0xA1)
 * 0 (Ack)
 * (Stop)
 
### ON
 
![](https://github.com/oritomov/cdc/blob/master/on.png)

 * 1000000 (7bit addrtess 0x40)
 * 0 (Write)
 * 0 (Ack)
 * 10100001 (8bit data 0xA1)
 * 0 (Ack)
 * 00100001 (8bit data 0x21)
 * 0 (Ack)
 * (Stop)

