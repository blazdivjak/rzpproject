__author__ = 'blaz'

import sys
import os
import time
import threading
import select
import sys
import pybonjour
import settings

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

"""
Loop forever, read arduino input and stream it to speakers
"""
while(1):

    time.sleep(5)

    #Get advertised speakers
    print browse.services

    #TODO: Read from Arduino

    #TODO: Create MIDI

    #TODO: Stream to sockets
