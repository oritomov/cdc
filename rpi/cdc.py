#!/usr/bin/python
import ConfigParser
import ctypes
import glob
import io
import os
import subprocess
import usb.core
import usb.util
from time import sleep
import select
import sys
import tty

MASS_STORAGE = 0x8
DEV_SD_STAR = "/dev/sd*"
USB_PATH = "/mnt/usb"
CDC_PATH = USB_PATH + "/cdc"
CONFIG = "config.ini"

tty.setcbreak(sys.stdin.fileno())

# detect a keypress
def poll_kb():
	key = ""
	if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
		key = sys.stdin.read(1)
		print key
	return key

# check devices for a class id
def find_dev(dev_class_id):
	device = usb.core.find()

	# is there a device at all
	if device is None:
		return False

	# check the device class
	if device.bDeviceClass == dev_class_id:
		return True

	# check configurations
	for cfg in device:
		# chack descriptors for interface class
		intf = usb.util.find_descriptor(cfg, bInterfaceClass=dev_class_id)
		if intf is not None:
			return True

	# found nothing
	return False

def mount():
	sd = glob.glob(DEV_SD_STAR)
	source = sd[0]
	target = USB_PATH
	fs = "vfat"
	options = ''
	ret = ctypes.CDLL('libc.so.6', use_errno=True).mount(source, target, fs, 0, options)
	if ret < 0:
		errno = ctypes.get_errno()
		#raise RuntimeError
		print("Error mounting {} ({}) on {} with options '{}': {}".
			format(source, fs, target, options, os.strerror(errno)))

# load the configuration file
def read_config(albumNum, trackNum):
	with open(CONFIG) as file:
		cfgfile = file.read()
	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.readfp(io.BytesIO(cfgfile))

	# list all contents
	#print("List all contents")
	#for section in config.sections():
	#	print("Section: %s" % section)
	#	for options in config.options(section):
	#		print("x %s:::%s:::%s" % (options,
	#								config.get(section, options),
	#								str(type(options))))

	albumNum = config.getint("cdc", 'album')  # Just get the value
	trackNum = config.getint("cdc", 'track')  # You know the datatype?

def write_config(albumNum, trackNum):
	# Check if there is already a configurtion file
	if os.path.isfile(CONFIG):
		if os.path.isfile(CONFIG + ".bak"):
			os.remove(CONFIG + ".bak")
		os.rename(CONFIG, CONFIG + ".bak")
	# Create the configuration file as it doesn't exist yet
	cfgfile = open(CONFIG, 'w')

	# Add content to the file
	config = ConfigParser.ConfigParser()
	config.add_section("cdc")
	config.set("cdc", "album", albumNum)
	config.set("cdc", "track", trackNum)
	config.write(cfgfile)
	cfgfile.close()

on = True
prev = False
next = False
usb_storage = False
tracks = None
player = None
albumNum = 0
trackNum = 0

# read cmds from the hu and act like a cd changer
while True:
	try:

		# key commands
		key = poll_kb()
		if (key != ""):
			if key == "1":
				on = not on
			elif key == "2":
				next = True
			elif key == "3":
				prev = True

		# find a usb storage
		if (not usb_storage) and find_dev(MASS_STORAGE):
			usb_storage = True
			print "found Mass Storage"

			if not os.path.exists(CDC_PATH):
				mount()

			tracks = None
			read_config(albumNum, trackNum)

		# tracks list
		if usb_storage and (tracks is None):
			albums = os.walk(CDC_PATH).next()[1]
			if albumNum > len(albums) - 1:
				albumNum = 0
				trackNum = 0
			if albumNum < 0:
				albumNum = len(albums) - 1
				trackNum = 0
			if len(albums) > 0:
				album = albums[albumNum]
			else:
				album = "."
			tracks = glob.glob(CDC_PATH + "/" + album + "/*.mp3")
			# TODO randomize
			player = None

		if (tracks is not None) and (trackNum >= len(tracks)):
			# next album
			albumNum = albumNum + 1
			trackNum = 0
			tracks = None

		if (tracks is not None) and (trackNum < 0):
			#prev album
			albumNum = albumNum - 1
			trackNum = 0
			tracks = None

		# start play
		if on and (tracks is not None) and (player is None):
			player = subprocess.Popen(["omxplayer",tracks[trackNum]],stdin=subprocess.PIPE) #,stdout=subprocess.PIPE,stderr=subprocess.PIPE
			write_config(albumNum, trackNum)

		#check playing
		if player is not None:
			fi = player.poll()
			if fi is not None:
				player = None
				# next track
				trackCount = len(tracks)
				trackNum = trackNum + 1

		# next
		if next and (player is not None):
			next = False
			player.stdin.write("q")
			player = None
			trackNum = trackNum + 1

		# prev
		if prev and (player is not None):
			prev = False
			player.stdin.write("q")
			player = None
			trackNum = trackNum - 1

		# stop play
		if not on and (player is not None):
			player.stdin.write("q") # test stop
			player = None

		sleep(0.1)

	except:
		usb_storage = False
		tracks = None
		player = None
		raise
