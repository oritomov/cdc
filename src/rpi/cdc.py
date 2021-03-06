#!/usr/bin/python
import ConfigParser
import ctypes
import glob
import io
import locale
import logging
import logging.config
import os
import RPi.GPIO as GPIO ## Import GPIO library
import usb.core
import usb.util
from time import sleep
import time

#import kbd as hu
import vag as hu
import child

#Sd Card
MASS_STORAGE = 0x8
#Bluetooth
WIRELESS_CONTROLLER = 0xE0

DEV_SD_STAR = '/dev/sd*'
USB_PATH = '/mnt/usb'
CDC_PATH = USB_PATH + '/music'
CONFIG = 'cdc.ini'
#GPIO_Pin = 7
#PIN_ON_TIME = 30

# create logger
logging.config.fileConfig('logging.cfg')
logger = logging.getLogger('root')

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
			logger.debug(sd)
			source = sd[0]
			if len(source) == 8:
				source = sd[1]
			break
		sleep(0.1)
	target = USB_PATH
	fs = 'vfat'
	options = ''
	ret = ctypes.CDLL('libc.so.6', use_errno=True).mount(source, target, fs, 0, options)
	if ret < 0:
		errno = ctypes.get_errno()
		#raise RuntimeError
		logger.error('Error mounting {} ({}) on {} with options \'{}\': {}'.
			format(source, fs, target, options, os.strerror(errno)))
	return

# load the configuration file
# fix it
def read_config(albumNum, trackNum):
	with open(CONFIG, 'r') as file:
		cfgfile = file.read()
	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.readfp(io.BytesIO(cfgfile))

	# list all contents
	#logger.info('List all contents')
	#logger.info('Sections: {}'.format(config.sections()))
	#for section in config.sections():
	#	logger.info('Section: {}'.format(section))
	#	logger.info('Options: {}'.format(config.options(section)))
	#	for option in config.options(section):
	#		val = config.get(section, option)
	#		if val == -1:
	#			logger.warning('skip: {}'.format(option))
	#		logger.info('read config: {} {} {}'.format(section, option, val))

	try:
		albumNum = config.getint('cdc', 'album')
		trackNum = config.getint('cdc', 'track')
		logger.info('read config album: {}, track: {}'.format(albumNum, trackNum))
	except:
		logger.warning('can\'t read config file')
	return [albumNum, trackNum]

# store the configuration file
def write_config(albumNum, trackNum):

	# Add content to the file
	config = ConfigParser.ConfigParser()
	config.add_section('cdc')
	config.set('cdc', 'album', albumNum)
	config.set('cdc', 'track', trackNum)

	# Create the configuration file as it doesn't exist yet
	with open(CONFIG, 'w') as file:
		config.write(file)

	logger.info('write config album: {}, track: {}'.format(albumNum, trackNum))
	return

# execute a command
def cmd(command):
	logger.debug(command)
	res = os.popen(command).read()
	if res is not None:
		logger.debug(res)
	return res

def shuffle(album):
	shuffle = '\'' + CDC_PATH + '/' + album + '/shuffle\''
	logger.info(shuffle)
	if not os.path.exists(shuffle):
		return True
	return False

# load new cd-dir
def play_cd(change, albumNum, trackNum, play):
	r = cmd('mpc ls')
	if r is not None:
		r = r.split('\n')
		logger.info('found {} albums'.format(len(r) - 1))
		if albumNum > len(r) - 2: # there is an empty line at the end
			albumNum = 0
			trackNum = 1
		if albumNum < 0:
			albumNum = len(r) - 2 # there is an empty line at the end
			trackNum = 1
		album = r[albumNum]
		logger.info(album)
		write_config(albumNum, trackNum)
		cmd('mpc clear')
		if shuffle(album):
			cmd('mpc listall \'' + album + '\' | shuf | mpc add')
		else:
			cmd('mpc listall \'' + album + '\' | mpc add')
#		cmd('mpc volume 100')
		if play:
			cmd('mpc play ' + str(trackNum))
			hu.set_status(albumNum, trackNum)
		else:
			cmd('mpc pause')
		logger.info('debug: album: {}, track: {}'.format(albumNum, trackNum))
	return [albumNum, trackNum]

#logging.basicConfig(filename='cdc.log',level=logging.INFO)
#logging.basicConfig(level=logging.INFO)
usb_storage = False
bluetooth = False
albumNum = 0
trackNum = 1
play = False
hu.connect()
#GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
#GPIO.setup(GPIO_Pin, GPIO.OUT) ## Setup GPIO Pin to OUT
#GPIO.output(GPIO_Pin, True) ## Turn on GPIO pin
#t = time.time()

# read hu commands from the vag and act like a cd changer
while True:
	try:
#		if ((t + PIN_ON_TIME) <  time.time()):
#			GPIO.output(GPIO_Pin, False) ## Turn on GPIO pin
		
		# get hu commands
		cdc_cmd = hu.get_command()

		# find a bluetooth 
		if (not bluetooth) and find_dev(WIRELESS_CONTROLLER):
			logger.info('found bluetooth')
			btSource = 'bluez_source.30_75_12_8A_D4_A0'
			btSink = 'alsa_output.platform-soc_sound.analog-stereo'
			#bt_command = 'pactl load-module module-loopback source={} sink={}'.format(btSource, btSink)
			bt_command = 'pactl load-module module-loopback'
			#child.main(['pi', '/home/pi', bt_command])
			bluetooth = True

		# find a usb storage
		if (not usb_storage) and find_dev(MASS_STORAGE):
			usb_storage = True
			logger.info('found Mass Storage')

			if not os.path.exists(CDC_PATH):
				mount()

			cmd('mpd /home/pi/.mpd/mpd.conf') #restart mpd
#			r = cmd('mpc update music')
#			logger.info(r)

			nums = read_config(albumNum, trackNum)
			albumNum = nums[0]
			trackNum = nums[1]
			logger.debug('read from config album: {}, track: {}'.format(albumNum, trackNum))
			nums = play_cd(None, albumNum, trackNum, play)
			albumNum = nums[0]
			trackNum = nums[1]

		if usb_storage and not find_dev(MASS_STORAGE):
			logger.warning('missing Mass Storage')
			cmd('mpc stop')
			usb_storage = False
			#cmd('mpc stop')

		if cdc_cmd == hu.HU_PLAY:
			play = True
#			GPIO.output(GPIO_Pin, False) ## Turn on GPIO pin
		elif cdc_cmd == hu.HU_STOP:
			play = False

		if usb_storage:
			# start play
			if cdc_cmd == hu.HU_PLAY:
				cmd('mpc play')
				trackNum = None # in order to set status

			# stop play
			elif cdc_cmd == hu.HU_STOP:
				cmd('mpc pause')

			if play:
				# next
				if cdc_cmd == hu.HU_NEXT:
					cmd('mpc next')

				# prev
				elif cdc_cmd == hu.HU_PREV:
					cmd('mpc prev')

				# next
				elif cdc_cmd == hu.HU_SEEK_FWD:
					while(1):
						cmd('mpc seek +00:00:10')
						if hu.get_command() is not None:
							break

				# prev
				elif cdc_cmd == hu.HU_SEEK_RWD:
					while(1):
						cmd('mpc seek -00:00:10')
						if hu.get_command() is not None:
							break

				elif cdc_cmd == hu.HU_CD1:
					nums = play_cd(albumNum, 0, 1, play)
					albumNum = nums[0]
					trackNum = nums[1]

				elif cdc_cmd == hu.HU_CD2:
					nums = play_cd(albumNum, 1, 1, play)
					albumNum = nums[0]
					trackNum = nums[1]

				elif cdc_cmd == hu.HU_CD3:
					nums = play_cd(albumNum, 2, 1, play)
					albumNum = nums[0]
					trackNum = nums[1]

				elif cdc_cmd == hu.HU_CD4:
					nums = play_cd(albumNum, 3, 1, play)
					albumNum = nums[0]
					trackNum = nums[1]

				elif cdc_cmd == hu.HU_CD5:
					nums = play_cd(albumNum, 4, 1, play)
					albumNum = nums[0]
					trackNum = nums[1]

				elif cdc_cmd == hu.HU_CD6:
					nums = play_cd(albumNum, 5, 1, play)
					albumNum = nums[0]
					trackNum = nums[1]

				elif cdc_cmd == hu.HU_NEXT_CD:
					nums = play_cd(None, albumNum + 1, 1, play)
					albumNum = nums[0]
					trackNum = nums[1]

				elif cdc_cmd == hu.HU_PREV_CD:
					nums = play_cd(None, albumNum - 1, 1, play)
					albumNum = nums[0]
					trackNum = nums[1]

				elif cdc_cmd == hu.HU_SCAN:
					cmd('mpc update')

				elif cdc_cmd == hu.HU_SHFFL:
					cmd('mpc random on')

				elif cdc_cmd == hu.HU_SEQNT:
					cmd('mpc random off')

				#check playing
				r = cmd('mpc |grep ] #')
				if (r is not None) and (len(r) > 0):
					# r='[playing] #18/37   1:53/4:50 (38%)'
					r = r.split('/')
					# r='[playing] #18', '37   1:53', '4:50 (38%)
					timer = None
					if len(r) > 2:
						timer = r[2].split(' ')[0]
					r = r[0].split('#')
					# r='[playing] ', '18'
					if len(r) > 1:
						tr = locale.atoi(r[1])
						#hu.set_status(albumNum, trackNum, timer)
						if tr != trackNum:
							trackNum = tr
							write_config(albumNum, trackNum)
							hu.set_status(albumNum, trackNum, timer)
				else:
					albumNum = albumNum + 1
					trackNum = 1
					nums = play_cd(None, albumNum, trackNum, play)
					albumNum = nums[0]
					trackNum = nums[1]
			#if play
		#if usb_storage

		sleep(0.1)

	except (KeyboardInterrupt):
		hu.close()
		break

	except:
		usb_storage = False
		raise
