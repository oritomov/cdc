#!/usr/bin/python
import ConfigParser
import ctypes
import glob
import io
import os
import string
import subprocess
import usb.core
import usb.util
from time import sleep

import kbd as hu

MASS_STORAGE = 0x8
DEV_SD_STAR = "/dev/sd*"
USB_PATH = "/mnt/usb"
CDC_PATH = USB_PATH + "/cdc"
CONFIG = "cdc.ini"

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
	return
 
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
	print "read album: ", albumNum, ", track ", trackNum
	return

# store the configuration file
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
	print "write album: ", albumNum, ", track ", trackNum
	return

# execute a command
def cmd(command):
	res = os.popen(command).read()
	if res is not None:
		print res
	return res

# load new cd-dir
def play_cd(albumNum, trackNum):
	r = cmd("mpc ls")
	if r != "":
		if albumNum >= len(r):
			albumNum = 0
		if albumNum < 0:
			albumNum = len(r) - 1
		album = r[albumNum]
		trackNum = 0
		write_config(albumNum, trackNum)
		cmd("mpc clear")
		cmd("mpc ls \"" + album + "\" | mpc add")
	return

usb_storage = False
hu.connect()

# read hu commands from the vag and act like a cd changer
while True:
	try:

		# get hu commands
		cdc_cmd = hu.get_command()

		# find a usb storage
		if (not usb_storage) and find_dev(MASS_STORAGE):
			usb_storage = True
			print "found Mass Storage"

			if not os.path.exists(CDC_PATH):
				mount()

			cmd("mpd /home/pi/.mpd/mpd.conf") #restart mpd

			read_config(albumNum, trackNum)
			play_cd(albumNum, trackNum)

		if usb_storage and not find_dev(MASS_STORAGE):
			usb_storage = False
			#cmd("mpc stop")

		if usb_storage:
			# start play
			if cdc_cmd == hu.CDC_PLAY:
				cmd("mpc play")

			# stop play
			elif cdc_cmd == hu.CDC_STOP:
				cmd("mpc pause")

			# next
			elif cdc_cmd == hu.CDC_NEXT:
				cmd("mpc next")

			# prev
			elif cdc_cmd == hu.CDC_PREV:
				cmd("mpc prev")

			# next
			elif cdc_cmd == hu.CDC_SEEK_FWD:
				while(1):
					cmd("mpc seek +00:00:10")
					if hu.get_command() is not None:
						break

			# prev
			elif cdc_cmd == hu.CDC_SEEK_RWD:
				while(1):
					cmd("mpc seek -00:00:10")
					if hu.get_command() is not None:
						break
 
			elif cdc_cmd == hu.CDC_CD1:
				play_cd(1)

			elif cdc_cmd == hu.CDC_CD2:
				play_cd(2)
 
			elif cdc_cmd == hu.CDC_CD3:
				play_cd(3)
 
			elif cdc_cmd == hu.CDC_CD4:
				play_cd(4)
 
			elif cdc_cmd == hu.CDC_CD5:
				play_cd(5)
 
			elif cdc_cmd == hu.CDC_CD6:
				play_cd(6)

			elif cdc_cmd == hu.CDC_SCAN:
				cmd("mpc update")

			elif cdc_cmd == hu.CDC_SHFFL:
				cmd("mpc random on")

			elif cdc_cmd == hu.CDC_SEQNT:
				cmd("mpc random off")

			#check playing
			r = cmd("mpc |grep ] #")
			if r is not None:
				r = r.split("/", 1)
				r = r[0].split("#", 1)
				tr = string.atoi(r[1])
				#hu.set_status(albumNum, trackNum, timer)
				if tr != trackNum:
					trackNum = tr
					write_config(albumNum, trackNum)
					hu.set_status(albumNum, trackNum)
			else:
				albumNum++
				trackNum = 0
				play_cd(albumNum, trackNum)
		#if usb_storage

		sleep(0.1)

	except (KeyboardInterrupt):
        hu.close()
		break

	except:
		usb_storage = False
		raise
