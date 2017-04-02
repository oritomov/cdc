# Emulator (Arduino & Raspbery Pi) for<br>Audi Gamma CC Bose CD Changer 

### Preface

This isn't my biggest project, but it is most compicated and ralated to too much unknown things my project. It is my first Python code and my first Arduno project. 

Audi Gamma CC Bose (HU) is my auto cassete player. It has ability to rule a CD Cahnger, not directly, but via specific Audi Interface (AI).

Even dought comunication with VAG's CD Changers is prety well documentad, I couldn't find any informatioan about comunication between my HU and the AI. I found out how the HU trys to comunicate to the AI, but I have not idea what the AI should reply. I will be verry apritiate if some kind person records the comunication and send it to me. This will be great help in order my emulator to shows played track and album number. At the moment it works without this.

The HU sends I2C/TWI signals to AI on 950 Hz (or sort of) to the address 0x40. ON is two bytes 0xA1 and 0x21, OFF is same bytes back order. Other signals what I riddle are from buttons '^', 'v', '>>' and '<<'. There is two more signals, one when HU doesnt like comunication - I called "Cansel", and one more, but I have no idea when and why HU sends it.

I implement the emulator from Arduino to replace the AI and Raspbery Pi to replace the CD Changer. I use separate DAC because those build in RPi is ... noy good enough.

Comunication between the Arduino and RPi is serial UART simular (but not same) to standard CDC communication.

Comunication between the RPi and the DAC what I choise, indeed PCB5102A, is via I2S.

I've made a special PCB to hold everything. The connector to the HU is hand made 10 pins simular to common ISO connector.

Power is based on LM2575-5.

Note: There is a trick. First hand shake of the HU comes around 0.4 seconds after HU power on. The Arduino takes more time for boot. Thats why I add two NPN transistors - one in order to lower akcnolege bit of I2C/TWI comunication, and anoter one to cancel this after Arduino's boot.

### Hardware
#### Audi Gamma CC Bose - Head Unit (HU)

![](https://github.com/oritomov/cdc/blob/master/etc/img/Audo%20Gamma%20CC%20Bose.jpg?raw=true)

#### Audi Interface 4A0 035 239, Blaupunkt 7 607 765 082 (AI) 

![](https://github.com/oritomov/cdc/blob/master/etc/img/4A0%20035%20239.jpg)
![](https://github.com/oritomov/cdc/blob/master/etc/img/Blaupunkt%207%20607%20765%20082.jpg)

#### CD Changer (CDC)

![](https://github.com/oritomov/cdc/blob/master/etc/img/CD_changer.jpg)

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

### Emulator

![](https://github.com/oritomov/cdc/blob/master/etc/img/emulator.png)

### Circuit

![](https://github.com/oritomov/cdc/blob/master/etc/cir/circuit.png)

### Beta

![](https://github.com/oritomov/cdc/blob/master/etc/img/DSC_0578.JPG)

### PCB

![](https://github.com/oritomov/cdc/blob/master/etc/pcb/cdc11.png)

### Release Candidate #1

![](https://github.com/oritomov/cdc/blob/master/etc/img/pcb_rel_1.JPG)
![](https://github.com/oritomov/cdc/blob/master/etc/img/asm_rel_1.JPG)

### Test

[![Release Candidate Test](https://www.youtube.com/upload_thumbnail?v=TbPQ_YEeIYg&t=hqdefault&ts=1491150349312)](https://www.youtube.com/watch?v=TbPQ_YEeIYg "Release Candidate Test")

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
