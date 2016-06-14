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

play=True
device=None
pt=0

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
#while True:
if True:
	try:

		if play:
			print "play"

			# find a device
			if (device == None) and find_dev(MASS_STORAGE):
				device = MASS_STORAGE
				print "found Mass Storage"

				if not os.path.exists(CDC_PATH):
					sd = glob.glob(DEV_SD_STAR)
					mount(sd[0], USB_PATH, "vfat")

				# tracks list
				f = glob.glob(CDC_PATH + "/*.mp3")

				# play
				player = subprocess.Popen(["omxplayer",f[pt]],stdin=subprocess.PIPE) #,stdout=subprocess.PIPE,stderr=subprocess.PIPE
				fi = player.poll()
				print fi

				sleep(5.0)
				player.stdin.write("q") # test stop
			else:
				print "Nothing"

		else:
			print "waiting"
			#sleep(0.5)

	except:
		raise
