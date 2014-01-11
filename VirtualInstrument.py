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
import serial
import datetime, time
from lib import MyMidiObject

class BrowseService(threading.Thread):
    """
    Class for browsing services advertised using Bonjour (MDNS) It runs in a seperate thread in the background
    """
    def __init__(self, regType):
        threading.Thread.__init__(self)
        self.regType = regType
        self.resolved = []
        self.timeout = 5
        self.services = {}
    def run(self):
        print "Starting thread"
        self.resolve_service(self.regType)

    def resolve_callback(self, sdRef, flags, interfaceIndex, errorCode, fullname,
                         hosttarget, port, txtRecord):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            #print 'Resolved service:'
            #print '  fullname   =', fullname
            #print '  hosttarget =', hosttarget
            #print '  port       =', port
            self.services[fullname.split('.')[0]]={'fullname': fullname, 'hosttarget': hosttarget, 'port': port}
            self.resolved.append(True)


    def browse_callback(self, sdRef, flags, interfaceIndex, errorCode, serviceName,
                        regtype, replyDomain):
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return

        if not (flags & pybonjour.kDNSServiceFlagsAdd):
            print 'Service removed'
            if serviceName in self.services.keys():
                del self.services[serviceName]
            return

        print 'Service added; resolving'

        resolve_sdRef = pybonjour.DNSServiceResolve(0,
                                                    interfaceIndex,
                                                    serviceName,
                                                    regtype,
                                                    replyDomain,
                                                    self.resolve_callback)

        try:
            while not self.resolved:
                ready = select.select([resolve_sdRef], [], [], self.timeout)
                if resolve_sdRef not in ready[0]:
                    print 'Resolve timed out'
                    break
                pybonjour.DNSServiceProcessResult(resolve_sdRef)
            else:
                self.resolved.pop()
        finally:
            resolve_sdRef.close()

    #python browseServices.py _VirtualSpeaker._udp
    def resolve_service(self, regtype='_VirtualSpeaker._udp'):
        browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
                                                  callBack = self.browse_callback)

        try:
            try:
                while True:
                    ready = select.select([browse_sdRef], [], [])
                    if browse_sdRef in ready[0]:
                        pybonjour.DNSServiceProcessResult(browse_sdRef)
            except KeyboardInterrupt:
                pass
        finally:
            browse_sdRef.close()

#####
#MAIN
#####

#Start background Service Resolution (Searching for speakers)
browse = BrowseService(settings.SERVICE_NAME)
browse.start()

#Initialize UDP SERVER

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

"""
Loop forever, read arduino input and stream it to speakers
"""
# serial port settings
ser = serial.Serial('/dev/ttyACM0', 9600)
then = datetime.datetime.now() + datetime.timedelta(seconds=2)
keysPressed = list()
while(1):

    #time.sleep(5)

    #Get advertised speakers
    #print browse.services

    #Read from Arduino
    line = ser.readline()
    line = line.split('\t')
    '''print line[0], "ms ",
    for i in line[1:]:
        if int(i) > 300:
            print 1,'\t',
        else:
            print 0,'\t',
    print '''
    try:
        lineBool = [True if int(x) > 300 else False for x in line[1:]]
    except Exception, err:
        lineBool = [False for x in line[1:]]
        print "Napaka: ", err.message
    #print "debug", lineBool
    if len(keysPressed) == 0:
        keysPressed = [False for x in range(len(lineBool))]
    #Stream to sockets

    #msg = raw_input('Enter message to send : ')
    #print browse.services.items()
    for key,value in browse.services.items():
        try :
            #Set the whole string
            for i in range(min(len(lineBool), len(keysPressed))):
                #print "lineBoolLen:", len(lineBool), " keyPressedLen:", len(keysPressed), " i:",i
                if lineBool[i] != keysPressed[i]:
                    msg = settings.FIRST_NOTE + i
                    #print "Sending message to ",value['hosttarget'] ,"on port ",value['port'], ": ", str(msg)
                    s.sendto(str(msg), (value['hosttarget'], value['port']))
            if (then < datetime.datetime.now()):
                msg = "init:" + str(settings.INSTRUMENT_ID)
                s.sendto(msg, (value['hosttarget'], value['port']))
                #print "Init sent to ", value['hosttarget']


        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        except Exception, msg:
            print msg.message
    keysPressed = lineBool
    if (then < datetime.datetime.now()):
        then = datetime.datetime.now() + datetime.timedelta(seconds=2)