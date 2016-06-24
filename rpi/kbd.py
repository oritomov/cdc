import select
import sys
import tty

# bytes sent when radio keys are pressed
CDC_PLAY     = chr(0xE4)
CDC_STOP     = chr(0x10)
CDC_NEXT     = chr(0xF8)
CDC_PREV     = chr(0x78)
CDC_SEEK_FWD = chr(0xD8)
CDC_SEEK_RWD = chr(0x58)
CDC_CD1      = chr(0x0C)
CDC_CD2      = chr(0x8C)
CDC_CD3      = chr(0x4C)
CDC_CD4      = chr(0xCC)
CDC_CD5      = chr(0x2C)
CDC_CD6      = chr(0xAC)
CDC_SCAN     = chr(0xA0)
CDC_SHFFL    = chr(0x60)
CDC_SEQNT    = chr(0x08)

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
			print "play"
			return CDC_PLAY
		elif key == "2":
			print "stop"
			return CDC_STOP
		elif key == "3":
			print "next"
			return CDC_NEXT
		elif key == "4":
			print "prev"
			return CDC_PREV
		elif key == "5":
			print "forward"
			return CDC_SEEK_FWD
		elif key == "6":
			print "reward"
			return CDC_SEEK_RWD
	return None

# display status
def set_status(albumNum, trackNum):
	return
