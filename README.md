# Emulator (Arduino & Raspbery Pi) for<br>Audi Gamma CC Bose CD Changer 

### Hardware
#### Audi Gamma CC Bose - Head Unit (HU)

![](https://github.com/oritomov/cdc/blob/master/etc/img/Audo%20Gamma%20CC%20Bose.jpg?raw=true)

#### Audi Interface 4A0 035 239, Blaupunkt 7 607 765 082 (AI) 

![](https://github.com/oritomov/cdc/blob/master/etc/img/4A0%20035%20239.jpg)
![](https://github.com/oritomov/cdc/blob/master/etc/img/Blaupunkt%207%20607%20765%20082.jpg)

#### CD Changer (CDC)

![](https://github.com/oritomov/cdc/blob/master/etc/img/CD_changer.jpg)

### Emulator

![](https://github.com/oritomov/cdc/blob/master/etc/img/emulator.png)

### Circuit

![](https://github.com/oritomov/cdc/blob/master/etc/cir/circuit.png)

### PCB

![](https://github.com/oritomov/cdc/blob/master/etc/pcb/cdc10.png)


### Beta

![](https://github.com/oritomov/cdc/blob/master/etc/img/DSC_0578.JPG)

### Release Candidate #1

![](https://github.com/oritomov/cdc/blob/master/etc/img/pcb_rel_1.JPG)
![](https://github.com/oritomov/cdc/blob/master/etc/img/asm_rel_1.JPG)

### I2C/TWI communication betwwen HU and AI
#### OFF

![](https://github.com/oritomov/cdc/blob/master/etc/img/off.png)

 * 1000000 (7bit addrtess 0x40)
 * 0 (Write)
 * 0 (Ack)
 * 00100001 (8bit data 0x21)
 * 0 (Ack)
 * 10100001 (8bit data 0xA1)
 * 0 (Ack)
 * (Stop)
 
#### ON
 
![](https://github.com/oritomov/cdc/blob/master/etc/img/on.png)

 * 1000000 (7bit addrtess 0x40)
 * 0 (Write)
 * 0 (Ack)
 * 10100001 (8bit data 0xA1)
 * 0 (Ack)
 * 00100001 (8bit data 0x21)
 * 0 (Ack)
 * (Stop)

### References

 * [VAG CDC Faker](http://dev.shyd.de/2013/09/avr-raspberry-pi-vw-beta-vag-cdc-faker/)
 * [Nick Gammon's page about I2C](http://gammon.com.au/i2c)
 * [Raspberry Pi rev2 template with mounting holes](https://www.raspberrypi.org/blog/raspberry-pi-rev2-template-with-mounting-holes/)
 * efficient 12V to 5V convertor [LM2575](http://www.ti.com.cn/cn/lit/ds/symlink/lm1575.pdf)
 * DAC [PCM5102A](https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=57069)  ([Beyond ES9023 PCM1794](https://www.google.bg/search?q=Beyond+ES9023+PCM1794))

### Utilities

 * [TinyCAD](https://sourceforge.net/projects/tinycad/)
 * [FreePcb](http://www.freepcb.com/)
 
### Special Thanks

 * ALOHAta
