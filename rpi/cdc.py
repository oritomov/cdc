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

on=True
device=None
tracks=None
player=None
trackNum=0

def mount(source, target, fs, options=''):
	ret = ctypes.CDLL('libc.so.6', use_errno=True).mount(source, target, fs, 0, options)
	if ret < 0:
		errno = ctypes.get_errno()
		#raise RuntimeError
		print("Error mounting {} ({}) on {} with options '{}': {}".
			format(source, fs, target, options, os.strerror(errno)))

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

# read cmds from the radio and act like a cd changer
while True:
#if True:
	#try:

		# start play
		if on and player is None:

			# find a device
			if (device is None) and find_dev(MASS_STORAGE):
				device = MASS_STORAGE
				print "found Mass Storage"

				if not os.path.exists(CDC_PATH):
					sd = glob.glob(DEV_SD_STAR)
					mount(sd[0], USB_PATH, "vfat")
					print "muont Mass Storage"

			# tracks list
			if (device is not None) and (tracks is None):
				tracks = glob.glob(CDC_PATH + "/*.mp3")
				print "found ", len(tracks), "tracks"

			# play
			if (tracks is not None) and (player is None):
				# play
				player = subprocess.Popen(["omxplayer",tracks[trackNum]],stdin=subprocess.PIPE) #,stdout=subprocess.PIPE,stderr=subprocess.PIPE
				print "play " + tracks[trackNum]

		#check playing
		if (player is not None):
			fi = player.poll()
			#print fi
			if fi is not None:
				player = None
				# next track
				trackCount = len(tracks)
				trackNum = trackNum + 1
				if trackNum > trackCount - 1:
					trackNum = 0
				print "start ", tracks[trackNum]

		# stop play
		if not on and player is not None:
			player.stdin.write("q") # test stop
			player = None

		#print "wait"
		sleep(0.1)

	#except:
	#	raise
