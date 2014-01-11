__author__ = 'blaz'

#Settings
PORT = 3333
HOST=''
SPEAKER_NAME = 'rpiDeviceX'
SERVICE_NAME = '_VirtualSpeaker._udp'
# ID codes: http://www.ccarh.org/courses/253/handout/gminstruments/
INSTRUMENT_ID = 0
FIRST_NOTE = 60
LOG_FOLDER='log/'
LOG_NAME='virtualdevice.log'
SERIAL_PORT='/dev/ttyACM0'
BAUD_RATE = 9600
MIDI_DEVICE=6 #8 on ubuntu, 6 on rpi
PLAY_DELAY=0 #200 for local play
CAPACITIVE_LIMIT=500
