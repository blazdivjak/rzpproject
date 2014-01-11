import logging
from setuptools.command.build_ext import if_dl
from numpy.core.multiarray import zeros

__author__ = 'blaz'

import sys
import os
import time
import threading
import select
import sys
import pybonjour
import settings
import socket
import pygame
import pygame.midi
from logger import *

class VirtualInstrument(threading.Thread):
    """
    Class for playing virtual instrument bonded via socket
    """
    """ midi instrument codes
    0   GRAND_PIANO
    19  CHURCH_ORGAN
    115 STEEL_DRUMS
    """

    instrument = 0
    hostname = ""
    channel = 0
    midi_out = None
    keyPressed = [False for _ in range(128)]
    def __init__(self, hostname, midi_out, instrument=0, channel=0):
        try:
            self.instrument = int(instrument.split(':')[1])
        except Exception, err:
            logging.error("Instrument ni pravilnega tipa, Details: %s", err.message)
        self.hostname = hostname
        self.channel = channel
        self.midi_out = midi_out
        try:
            self.midi_out.set_instrument(self.instrument, self.channel)
        except Exception, err:
            logging.error(err.message)
            #print err.message

    def processData(self, data):
        if "init:" in data:
            pass
        else:
            try:
                nota = int(data)
                self.keyPressed[nota] = not self.keyPressed[nota]
                if self.keyPressed[nota]:
                    self.midi_out.note_on(nota, 127, channel=self.channel)
                    #logging.info("Note %d on channel %d is ON", nota, self.channel)
                else:
                    self.midi_out.note_off(nota, 127, channel=self.channel)
                    #logging.info("Note %d on channel %d is OFF", nota, self.channel)
            except Exception:
                logging.error("Received data is not in correct form.")

class AdvertiseService(threading.Thread):
    """
    Class for advertising service using Bonjour (MDNS). It runs in a seperate thread in the background
    """
    def __init__(self, name='rpiSpeaker01', regType='_VirtualSpeaker._udp', port=3333):
        threading.Thread.__init__(self)
        self.name = name
        self.regType = regType
        self.port = port
    def run(self):
        logging.info("Starting Bonjour service advertising thread")
        self.register_service(self.name, self.regType, self.port)

    def register_callback(self, sdRef, flags, errorCode, name, regtype, domain):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            logging.info('Started VirtualSpeaker Service:')
            logging.info('  name    =%s', name)
            logging.info('  regtype =%s', regtype)
            logging.info('  domain  =%s', domain)

    def register_service(self, name='rpiSpeaker01', regtype='_VirtualSpeaker._udp', port=3333):
        sdRef = pybonjour.DNSServiceRegister(name = name,
                                             regtype = regtype,
                                             port = port,
                                             callBack = self.register_callback)

        try:
            try:
                while True:
                    ready = select.select([sdRef], [], [])
                    if sdRef in ready[0]:
                        pybonjour.DNSServiceProcessResult(sdRef)
            except KeyboardInterrupt:
                pass
        finally:
            sdRef.close()

class InitTimidity(threading.Thread):
    """
    Class for software synthesizer timidity. It runs in a seperate thread in the background
    """
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        logging.info("Starting TiMidity in ALSA server mode")
        try:
            os.system("timidity -iA")
        except Exception as err:
            logging.error("Cant start softsynth, %s", err)
            exit()

#####
#MAIN
#####

#Start background Service Advertisment
register = AdvertiseService(name=settings.SPEAKER_NAME, port=settings.PORT)
logging.info("Starting VirtualDevice named: %s", settings.SPEAKER_NAME)
register.daemon = True
register.start()

logging.info("Initializing pygame midi")
try:
    pygame.init()
    pygame.midi.init()
    #port = pygame.midi.get_default_output_id()
    port = settings.MIDI_DEVICE
    logging.info("Using midi output_id :%s:", port)
    midi_out = pygame.midi.Output(port, 0)
except Exception as err:
    logging.error(err)
    exit()

#Initialize Timidity software synthesizer to output music to your soundcard
#timidity = InitTimidity()
#timidity.daemon = True
#timidity.start()

#Initialize UDP SERVER
port = settings.PORT
host = settings.HOST

# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logging.info('Socket created')
except socket.error, msg :
    logging.error('Failed to create socket. Error Code : %s message: %s',str(msg[0]), msg[1])
    sys.exit()

# Bind socket to local host and port
try:
    s.bind((host, port))
except socket.error , msg:
    logging.fatal('Bind failed. Error Code : %s message: %s', str(msg[0]),msg[1])
    sys.exit()

logging.info('Socket bind complete')

logging.info("Waiting on port: %s", port)

#Check for connection loss and remove virtual instrument accordingly
longtimeNoSee = list()

#Virtual instrument list
virtualInstruments = dict()

newChannel = 0
"""
Loop forever
"""
while(1):

    #Read from socket
    data, addr = s.recvfrom(1024)

    #Virtual instrument missing from client list
    if addr not in virtualInstruments.keys():
        if "init:" in data:
            print("Added instument:", addr, " ", data, " on channel: ", newChannel)
            virtualInstruments.setdefault(addr, VirtualInstrument(hostname=addr, midi_out=midi_out,  instrument=data, channel=newChannel))
            logging.info("Virtual instrument with instrument_id: %s added.", data.split(':')[1])
            newChannel += 1
    else:
        virtualInstruments[addr].processData(data)
    if False:
        if not virtualInstruments[addr].processData(data):
            del virtualInstruments[addr]

    #print addr, ": ", data, "    dict ", virtualInstruments


s.close()


