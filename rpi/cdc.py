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

import kbd as cmds

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
	return

usb_storage = False
cmds.connect()

# read cmds from the hu and act like a cd changer
while True:
	try:

		# get commands
		cdc_cmd = cmds.get_command()

		# find a usb storage
		if (not usb_storage) and find_dev(MASS_STORAGE):
			usb_storage = True
			print "found Mass Storage"

			if not os.path.exists(CDC_PATH):
				mount()

			r = os.popen("mpd /home/pi/.mpd/mpd.conf").read() #restart mpd
			if r is not None:
				print r
			r = os.popen("mpc pause").read()
			if r is not None:
				print r
			r = os.popen("mpc update").read()
			if r is not None:
				print r

		# start play
		if usb_storage and cdc_cmd == cmds.CDC_PLAY:
			r = os.popen("mpc play").read()
			if r is not None:
				print r

		# stop play
		elif usb_storage and cdc_cmd == cmds.CDC_STOP:
			r = os.popen("mpc pause").read()
			if r is not None:
				print r

		# next
		elif usb_storage and cdc_cmd == cmds.CDC_NEXT:
			r = os.popen("mpc next").read()
			if r is not None:
				print r

		# prev
		elif usb_storage and cdc_cmd == cmds.CDC_PREV:
			r = os.popen("mpc prev").read()
			if r is not None:
				print r

		# next
		elif usb_storage and cdc_cmd == cmds.CDC_SEEK_FWD:
			while(1):
				os.popen("mpc seek +00:00:10")
				if cmds.get_command() is not None:
					break

		# prev
		elif usb_storage and cdc_cmd == cmds.CDC_SEEK_RWD:
			while(1):
				os.popen("mpc seek -00:00:10")
				if cmds.get_command() is not None:
					break

		elif usb_storage and cdc_cmd == cmds.CDC_SCAN:
			r = os.popen("mpc update").read()
			if r is not None:
				print r

		elif usb_storage and cdc_cmd == cmds.CDC_SHFFL:
			r = os.popen("mpc random on").read()
			if r is not None:
				print r

		elif usb_storage and cdc_cmd == cmds.CDC_SEQNT:
			r = os.popen("mpc random off").read()
			if r is not None:
				print r

		#check playing
		if usb_storage:
			r = os.popen("mpc").read()
			if r is None:
				print "stopped"

		sleep(0.1)

	except:
		usb_storage = False
		raise
