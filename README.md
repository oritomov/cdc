# Emulator (Arduino & Raspbery Pi) for<br>Audi Gamma CC Bose CD Changer 

### Hardware
#### Audi Gamma CC Bose - Head Unit (HU)

![](https://github.com/oritomov/cdc/blob/master/Audo%20Gamma%20CC%20Bose.jpg)

#### Audi Interface 4A0 035 239, Blaupunkt 7 607 765 082 (AI) 

![](https://github.com/oritomov/cdc/blob/master/4A0%20035%20239.jpg)
![](https://github.com/oritomov/cdc/blob/master/Blaupunkt%207%20607%20765%20082.jpg)

#### CD Changer (CDC)

![](https://github.com/oritomov/cdc/blob/master/CD_changer.jpg)

### Emulator

![](https://github.com/oritomov/cdc/blob/master/emulator.png)

### Circuit

![](https://github.com/oritomov/cdc/blob/master/circuit.png)

### PCB

![](https://github.com/oritomov/cdc/blob/master/cdc6.png)
![](https://github.com/oritomov/cdc/blob/master/cdc6a.png)

### Beta

![](https://github.com/oritomov/cdc/blob/master/DSC_0577.JPG)

### I2C/TWI communication betwwen HU and AI
#### OFF

![](https://github.com/oritomov/cdc/blob/master/off.png)

 * 1000000 (7bit addrtess 0x40)
 * 0 (Write)
 * 0 (Ack)
 * 00100001 (8bit data 0x21)
 * 0 (Ack)
 * 10100001 (8bit data 0xA1)
 * 0 (Ack)
 * (Stop)
 
#### ON
 
![](https://github.com/oritomov/cdc/blob/master/on.png)

 * 1000000 (7bit addrtess 0x40)
 * 0 (Write)
 * 0 (Ack)
 * 10100001 (8bit data 0xA1)
 * 0 (Ack)
 * 00100001 (8bit data 0x21)
 * 0 (Ack)
 * (Stop)

### References

 * [Nick Gammon's page about I2C](http://gammon.com.au/i2c)
 * [How To Burn a Bootloader to Clone Arduino Nano 3.0](http://www.instructables.com/id/How-To-Burn-a-Bootloader-to-Clone-Arduino-Nano-30)
 * [Raspberry Pi rev2 template with mounting holes](https://www.raspberrypi.org/blog/raspberry-pi-rev2-template-with-mounting-holes/)
 * efficient 12V to 5V convertor [LM2575](http://www.ti.com/product/LM2575)
 * DAC [PCM5102A](https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=57069)

### Utilities

 * [TinyCAD](https://sourceforge.net/projects/tinycad/)
 * [FreePcb](http://www.freepcb.com/)
