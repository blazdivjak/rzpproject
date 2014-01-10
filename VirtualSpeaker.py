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

class VirtualInstrument():
    """
    Class for playing virtual instrument bonded via socket
    """
    """ midi instrument codes
    0   GRAND_PIANO
    19  CHURCH_ORGAN
    37  SLAP_BASS_1
    41  VIOLIN
    115 STEEL_DRUMS
    """

    instrument = 0
    hostname = ""
    midiDevice = -1
    midi_output = None
    keyPressed = [False for i in range(127)]
    def __init__(self, hostname, instrument=0, midiDevice=None):
        try:
            self.instrument = int(instrument.split(':')[1])
        except Exception, err:
            print "Instrument ni pravilnega tipa ", err.message
        self.hostname = hostname
        pygame.init()
        pygame.midi.init()
        if midiDevice == None:
            self.midiDevice = pygame.midi.get_default_output_id()
        else:
            self.midiDevice = midiDevice
        print self.midiDevice, " ", type(self.midiDevice)
        self.midi_out = pygame.midi.Output(self.midiDevice, 0)
        try:
            self.midi_out.set_instrument(self.instrument)
        except Exception, err:
            print err.message

    def processData(self, data):
        if "init:" in data:
            # Refresh playing notes
            #self.refreshNotes()
            pass
        elif data == "off":
            keyPressed = [False for i in range(127)]
            self.refreshNotes()
            return False
        else:
            try:
                nota = int(data)
                self.keyPressed[nota] = not self.keyPressed[nota]
            except Exception:
                print "Prislo je do napake pri sprejemu podatkov - podatki niso pravilne oblike"
        self.refreshNotes()


    def refreshNotes(self):
        for i in range(len(self.keyPressed)):
            if self.keyPressed[i]:
                # note velocity is fixed
                print "Prizgana nota ", i
                self.midi_out.note_on(i,127)
            else:
                self.midi_out.note_off(i,127)

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
        print "Starting thread"
        self.register_service(self.name, self.regType, self.port)

    def register_callback(self, sdRef, flags, errorCode, name, regtype, domain):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            print 'Started VirtualSpeaker Service:'
            print '  name    =', name
            print '  regtype =', regtype
            print '  domain  =', domain

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

#####
#MAIN
#####

#Start background Service Advertisment
register = AdvertiseService(name=settings.SPEAKER_NAME, port=settings.PORT)
register.start()

#Initialize UDP SERVER
port = settings.PORT
host = settings.HOST

# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Bind socket to local host and port
try:
    s.bind((host, port))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

print "Waiting on port:", port

#Check for connection loss and remove virtual instrument accordingly
longtimeNoSee = list()

#Virtual instrument list
virtualInstruments = dict()

channel = 0
"""
Loop forever
"""
while(1):

    #Read from socket
    data, addr = s.recvfrom(1024)

    #Virtual instrument missing from client list
    if addr not in virtualInstruments.keys():
        if "init:" in data:
            virtualInstruments.setdefault(addr, VirtualInstrument(hostname=addr, instrument=data))
            print "Virtual instrument with instrument_id:", data.split(':')[1], " added"
    else:
        virtualInstruments[addr].processData(data)
    if False:
        if not virtualInstruments[addr].processData(data):
            del virtualInstruments[addr]

    print addr, ": ", data, "    dict ", virtualInstruments


s.close()


