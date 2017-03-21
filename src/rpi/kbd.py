import logging
import select
import sys
import tty

# bytes sent when radio keys are pressed
HU_PLAY     = chr(0xE4)
HU_STOP     = chr(0x10)
HU_NEXT     = chr(0xF8)
HU_PREV     = chr(0x78)
HU_SEEK_FWD = chr(0xD8)
HU_SEEK_RWD = chr(0x58)
HU_CD1      = chr(0x0C)
HU_CD2      = chr(0x8C)
HU_CD3      = chr(0x4C)
HU_CD4      = chr(0xCC)
HU_CD5      = chr(0x2C)
HU_CD6      = chr(0xAC)
HU_SCAN     = chr(0xA0)
HU_SHFFL    = chr(0x60)
HU_SEQNT    = chr(0x08)

tty.setcbreak(sys.stdin.fileno())

# connect
def connect():
	return True

# close
def close():
	return True

# detect a keypress
def poll_kb():
	key = ""
	if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
		key = sys.stdin.read(1)
	return key

# key commands
def get_command():
	key = poll_kb()
	if (key != ""):
		if key == "1":
			logging.info("play")
			return HU_PLAY
		elif key == "2":
			logging.info("stop")
			return HU_STOP
		elif key == "3":
			logging.info("next")
			return HU_NEXT
		elif key == "4":
			logging.info("prev")
			return HU_PREV
		elif key == "5":
			logging.info("forward")
			return HU_SEEK_FWD
		elif key == "6":
			logging.info("reward")
			return HU_SEEK_RWD
	return None

# display status
def set_status(albumNum, trackNum):
	return
