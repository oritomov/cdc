// bytes sent when radio keys are pressed

// switch on in cd mode/radio to cd (play)
// 0x53 0x2C 0xE4 0x1B play
// 0x53 0x2C 0x14 0xEB end cmd
#define CDC_PLAY     (uint8_t)0xE4

// switch off in cd mode/cd to radio (pause)
// 0x53 0x2C 0x10 0xEF stop
// 0x53 0x2C 0x14 0xEB end cmd
#define CDC_STOP     (uint8_t)0x10

#define CDC_END_CMD  (uint8_t)0x14

// next
// 0x53 0x2C 0xF8 0x7
#define CDC_NEXT     (uint8_t)0xF8

// prev
// 0x53 0x2C 0x78 0x87
#define CDC_PREV     (uint8_t)0x78

// seek next
// 0x53 0x2C 0xD8 0x27 hold down
// 0x53 0x2C 0xE4 0x1B release
// 0x53 0x2C 0x14 0xEB end cmd
#define CDC_SEEK_FWD (uint8_t)0xD8

// seek prev
// 0x53 0x2C 0x58 0xA7 hold down
// 0x53 0x2C 0xE4 0x1B release
// 0x53 0x2C 0x14 0xEB end cmd
#define CDC_SEEK_RWD (uint8_t)0x58

// cd #
// 0x53 0x2C 0x#C 0x#3
// 0x53 0x2C 0x14 0xEB end cmd
// 0x53 0x2C 0x38 0xC7 cd set
// send new cd no. to confirm change, else:
// 0x53 0x2C 0xE4 0x1B beep, no cd (same as play)
// 0x53 0x2C 0x14 0xEB end cmd

// 0x53 0x2C 0x38 0xC7
#define CDC_CDSET    (uint8_t)0x38

// cd 1
// 0x53 0x2C 0x0C 0xF3
#define CDC_CD1      (uint8_t)0x0C

// cd 2
// 0x53 0x2C 0x8C 0x73
#define CDC_CD2      (uint8_t)0x8C

// cd 3
// 0x53 0x2C 0x4C 0xB3
#define CDC_CD3      (uint8_t)0x4C

// cd 4
// 0x53 0x2C 0xCC 0x33
#define CDC_CD4      (uint8_t)0xCC

// cd 5
// 0x53 0x2C 0x2C 0xD3
#define CDC_CD5      (uint8_t)0x2C

// cd 6
// 0x53 0x2C 0xAC 0x53
#define CDC_CD6      (uint8_t)0xAC

// scan (in 'sequential', 'shuffle' or 'scan' mode)
// 0x53 0x2C 0xA0 0x5F
#define CDC_SCAN     (uint8_t)0xA0

// shuffle in 'sequential' mode
// 0x53 0x2C 0x60 0x9F
#define CDC_SHFFL    (uint8_t)0x60

// sequential in 'shuffle' mode
// 0x53 0x2C 0x08 0xF7
// 0x53 0x2C 0x14 0xEB end cmd
#define CDC_SEQNT    (uint8_t)0x08



// bytes sent back to radio
// frame cd#   tr#   time  time  mode  frame frame
// 0x34, 0xBE, 0xFF, 0xFF, 0xFF, 0xFF, 0xCF, 0x3C
#define CDC_STATUS   (uint8_t)0x34

