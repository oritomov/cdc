#!/usr/bin/python
import configparser
import ctypes
import glob
import io
import locale
import logging
import os
import usb.core
import usb.util
from time import sleep

#import kbd as hu
import vag as hu

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
	while True:
		sd = glob.glob(DEV_SD_STAR)
		if len(sd) > 1:
			logging.debug(sd)
			source = sd[0]
			if len(source) == 8:
				source = sd[1]
			break
		sleep(0.1)
	target = USB_PATH
	fs = "vfat"
	options = ''
	ret = ctypes.CDLL('libc.so.6', use_errno=True).mount(source, target, fs, 0, options)
	if ret < 0:
		errno = ctypes.get_errno()
		#raise RuntimeError
		logging.error("Error mounting {} ({}) on {} with options '{}': {}".
			format(source, fs, target, options, os.strerror(errno)))
	return

# load the configuration file
def read_config(albumNum, trackNum):
	with open(CONFIG) as file:
		cfgfile = file.read()
	config = configparser.RawConfigParser(allow_no_value=True)
	config.readfp(io.BytesIO(cfgfile))

	# list all contents
	#print("List all contents")
	#for section in config.sections():
	#	print("Section: %s" % section)
	#	for options in config.options(section):
	#		print("x %s:::%s:::%s" % (options,
	#								config.get(section, options),
	#								str(type(options))))
	try:
		albumNum = config.getint("cdc", 'album')  # Just get the value
		trackNum = config.getint("cdc", 'track')  # You know the datatype?
		logging.info("read gonfig album: {}, track: {}".format(albumNum, trackNum))
	except:
		logging.warning("can\'t read config file")
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
	config = configparser.ConfigParser()
	config.add_section("cdc")
	config.set("cdc", "album", albumNum)
	config.set("cdc", "track", trackNum)
	config.write(cfgfile)
	cfgfile.close()
	logging.info("write config album: {}, track: {}".format(albumNum, trackNum))
	return

# execute a command
def cmd(command):
	logging.debug(command)
	res = os.popen(command).read()
	if res is not None:
		logging.debug(res)
	return res

# load new cd-dir
def play_cd(change, albumNum, trackNum, play):
	r = cmd("mpc ls")
	if r is not None:
		r = r.split("\n")
		logging.info("found {} albums".format(len(r) - 1))
		if albumNum > len(r) - 2: # there is an empty line at the end
			albumNum = 0
			trackNum = 1
		if albumNum < 0:
			albumNum = len(r) - 2 # there is an empty line at the end
			trackNum = 1
		album = r[albumNum]
		logging.info(album)
		write_config(albumNum, trackNum)
		cmd("mpc clear")
		cmd("mpc listall \"" + album + "\" | mpc add")
		cmd("mpc volume 100")
		cmd("mpc play " + str(trackNum))
		if not play:
			cmd("mpc pause")
	return

logging.basicConfig(filename='cdc.log',level=logging.INFO)
usb_storage = False
albumNum = 0
trackNum = 1
play = False
hu.connect()

# read hu commands from the vag and act like a cd changer
while True:
	try:

		# get hu commands
		cdc_cmd = hu.get_command()

		# find a usb storage
		if (not usb_storage) and find_dev(MASS_STORAGE):
			usb_storage = True
			logging.info("found Mass Storage")

			if not os.path.exists(CDC_PATH):
				mount()

			cmd("mpd /home/pi/.mpd/mpd.conf") #restart mpd

			read_config(albumNum, trackNum)
#TODO
			logging.debug("album: {}, track: {}".format(albumNum, trackNum))
			play_cd(None, albumNum, trackNum, play)

		if usb_storage and not find_dev(MASS_STORAGE):
			logging.warning("missing Mass Storage")
			usb_storage = False
			#cmd("mpc stop")

		if cdc_cmd == hu.HU_PLAY:
			play = True
		elif cdc_cmd == hu.HU_STOP:
			play = False

		if usb_storage:
			# start play
			if cdc_cmd == hu.HU_PLAY:
				cmd("mpc play")

			# stop play
			elif cdc_cmd == hu.HU_STOP:
				cmd("mpc pause")

			# next
			elif cdc_cmd == hu.HU_NEXT:
				cmd("mpc next")

			# prev
			elif cdc_cmd == hu.HU_PREV:
				cmd("mpc prev")

			# next
			elif cdc_cmd == hu.HU_SEEK_FWD:
				while(1):
					cmd("mpc seek +00:00:10")
					if hu.get_command() is not None:
						break

			# prev
			elif cdc_cmd == hu.HU_SEEK_RWD:
				while(1):
					cmd("mpc seek -00:00:10")
					if hu.get_command() is not None:
						break

			elif cdc_cmd == hu.HU_CD1:
				play_cd(0, albumNum, trackNum, play)

			elif cdc_cmd == hu.HU_CD2:
				play_cd(1, albumNum, trackNum, play)

			elif cdc_cmd == hu.HU_CD3:
				play_cd(2, albumNum, trackNum, play)

			elif cdc_cmd == hu.HU_CD4:
				play_cd(3, albumNum, trackNum, play)

			elif cdc_cmd == hu.HU_CD5:
				play_cd(4, albumNum, trackNum, play)

			elif cdc_cmd == hu.HU_CD6:
				play_cd(5, albumNum, trackNum, play)

			elif cdc_cmd == hu.HU_SCAN:
				cmd("mpc update")

			elif cdc_cmd == hu.HU_SHFFL:
				cmd("mpc random on")

			elif cdc_cmd == hu.HU_SEQNT:
				cmd("mpc random off")

			if play:
				#check playing
				r = cmd("mpc |grep ] #")
				if (r is not None) and (len(r) > 0):
					r = r.split("/", 1)
					r = r[0].split("#", 1)
					if len(r) > 1:
						tr = locale.atoi(r[1])
						#hu.set_status(albumNum, trackNum, timer)
						if tr != trackNum:
							trackNum = tr
							write_config(albumNum, trackNum)
							hu.set_status(albumNum, trackNum)
				else:
					albumNum = albumNum + 1
					trackNum = 1
					play_cd(None, albumNum, trackNum, play)
		#if usb_storage

		sleep(0.1)

	except (KeyboardInterrupt):
		hu.close()
		break

	except:
		usb_storage = False
		raise
