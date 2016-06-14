#!/usr/bin/python
import ctypes
import glob
import os
import subprocess
import usb.core
import usb.util
from time import sleep

MASS_STORAGE = 0x8
DEV_SD_STAR = "/dev/sd*"
USB_PATH = "/mnt/usb"
CDC_PATH = USB_PATH + "/cdc"

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

on = True
prev = False
next = False
device = None
tracks = None
player = None
albumNum = 0
trackNum = 0

# read cmds from the hu and act like a cd changer
while True:
	try:

		# find a device
		if (device is None) and find_dev(MASS_STORAGE):
			device = MASS_STORAGE
			print "found Mass Storage"

			if not os.path.exists(CDC_PATH):
				mount()
				tracks = None

		# tracks list
		if (device is not None) and (tracks is None):
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
			next = None
			player.stdin.write("q")
			player = None
			trackNo = trackNo + 1

		# prev
		if prev and (player is not None):
			prev = None
			player.stdin.write("q")
			player = None
			trackNo = trackNo - 1

		# stop play
		if not on and (player is not None):
			player.stdin.write("q") # test stop
			player = None

		sleep(0.1)

	except:
		device=None
		tracks=None
		player=None
		raise
