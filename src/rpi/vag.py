#!/usr/bin/python
import logging
import serial
import time

# bytes sent when radio keys are pressed

# switch on in cd mode/radio to cd (play)
# 0x53 0x2C 0xE4 0x1B
# 0x53 0x2C 0x14 0xEB
HU_PLAY     = chr(0xE4)

# switch off in cd mode/cd to radio (pause)
# 0x53 0x2C 0x10 0xEF
# 0x53 0x2C 0x14 0xEB
HU_STOP     = chr(0x10)

HU_END_CMD  = chr(0x14)

# next
# 0x53 0x2C 0xF8 0x7
HU_NEXT     = chr(0xF8)

# prev
# 0x53 0x2C 0x78 0x87
HU_PREV     = chr(0x78)

# seek next
# 0x53 0x2C 0xD8 0x27 hold down
# 0x53 0x2C 0xE4 0x1B release
# 0x53 0x2C 0x14 0xEB
HU_SEEK_FWD = chr(0xD8)

# seek prev
# 0x53 0x2C 0x58 0xA7 hold down
# 0x53 0x2C 0xE4 0x1B release
# 0x53 0x2C 0x14 0xEB
HU_SEEK_RWD = chr(0x58)

# cd #
# 0x53 0x2C 0x#C 0x#3
# 0x53 0x2C 0x14 0xEB
# 0x53 0x2C 0x38 0xC7
# send new cd no. to confirm change, else:
# 0x53 0x2C 0xE4 0x1B beep, no cd (same as play)
# 0x53 0x2C 0x14 0xEB

#0x53 0x2C 0x38 0xC7
HU_CDSET    = chr(0x38)

# cd 1
# 0x53 0x2C 0x0C 0xF3
HU_CD1      = chr(0x0C)

# cd 2
# 0x53 0x2C 0x8C 0x73
HU_CD2      = chr(0x8C)

# cd 3
# 0x53 0x2C 0x4C 0xB3
HU_CD3      = chr(0x4C)

# cd 4
# 0x53 0x2C 0xCC 0x33
HU_CD4      = chr(0xCC)

# cd 5
# 0x53 0x2C 0x2C 0xD3
HU_CD5      = chr(0x2C)

# cd 6
# 0x53 0x2C 0xAC 0x53
HU_CD6      = chr(0xAC)

# scan (in 'sequential', 'shuffle' or 'scan' mode)
# 0x53 0x2C 0xA0 0x5F
HU_SCAN     = chr(0xA0)

# shuffle in 'sequential' mode
# 0x53 0x2C 0x60 0x9F
HU_SHFFL    = chr(0x60)

# sequential in 'shuffle' mode
# 0x53 0x2C 0x08 0xF7
# 0x53 0x2C 0x14 0xEB
HU_SEQNT    = chr(0x08)

# NOTE! Those are two made up commands in order to change the CDs
HU_NEXT_CD  = chr(0x00)
HU_PREV_CD  = chr(0xFF)

global ser
ser = None
timeout_seek = 0.5
timeout_normal = 2

# init serial and last cd no. for correct radio display
def connect():
	while(1):
		try:
			global ser
			ser = serial.Serial('/dev/ttyAMA0', 9600)
			ser.timeout = timeout_normal #we need a timeout to update the track no.
			ser.writeTimeout = timeout_normal
			return
		except:
			time.sleep(2) #wait before retrying

# init serial and last cd no. for correct radio display
def close():
	ser.close()

# key commands
def get_command():
	c = ser.read()
	if c == "":
		return None
	elif (c == HU_PLAY) or (c == HU_STOP) or (c == HU_SEQNT):
		if ser.read() == HU_END_CMD:
			# stop seek
			ser.timeout = timeout_normal
			if (c == HU_PLAY):
				logging.info("serial play")
			elif (c == HU_STOP):
				logging.info("serial stop")
			elif (c == HU_SEQNT):
				logging.info("serial sequent")
			return c
	elif (c == HU_NEXT) or (c == HU_PREV):
		if (c == HU_NEXT):
			logging.info("serial next")
		elif (c == HU_PREV):
			logging.info("serial prev")
		return c
	elif (c == HU_SEEK_FWD) or  (c == HU_SEEK_RWD):
		ser.timeout = timeout_seek
		return c
	elif (c == HU_CD1) or (c == HU_CD2) or (c == HU_CD3) or (c == HU_CD4) or (c == HU_CD5) or (c == HU_CD6):
		if (ser.read() == HU_END_CMD) and (ser.read() == HU_CDSET):
			return c
	# NOTE! Those are two made up commands in order to change the CDs
	elif (c == HU_PREV_CD) or (c == HU_NEXT_CD):
		if (c == HU_NEXT_CD):
			logging.info("serial next cd")
		elif (c == HU_PREV_CD):
			logging.info("serial prev cd")
		return c
		
	#else
	logging.warning("serial: {}".format(c))

	return None

# frame cd#   tr#   time  time  mode  frame frame
# 0x34, 0xBE, 0xFF, 0xFF, 0xFF, 0xFF, 0xCF, 0x3C
def set_status(cd, track, timer):
	logging.info("serial return: cd {}, track {}, timer {}".format(cd, track, timer))
	return
