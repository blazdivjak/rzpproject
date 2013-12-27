__author__ = 'blaz'

import sys
import os
import time
import threading
import select
import sys
import pybonjour
import settings

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

"""
Loop forever
"""
while(1):
    time.sleep(60)
    print "This program continues to run!"




