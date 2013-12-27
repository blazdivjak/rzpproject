__author__ = 'blaz'

import select
import sys
import pybonjour

#python registerService.py Instrument _VirtualInstrument._udp 3333
#name    = sys.argv[1]
#regtype = sys.argv[2]
#port    = int(sys.argv[3])

#name = "rpiSpeaker01"
#regtype = "_VirtualSpeaker._udp"
#port = 3333

def register_callback(sdRef, flags, errorCode, name, regtype, domain):
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        print 'Started VirtualSpeaker Service:'
        print '  name    =', name
        print '  regtype =', regtype
        print '  domain  =', domain

def register_service(name='rpiSpeaker01', regtype='_VirtualSpeaker._udp', port=3333):
    sdRef = pybonjour.DNSServiceRegister(name = name,
                                         regtype = regtype,
                                         port = port,
                                         callBack = register_callback)

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


#main
register_service(name='rpiSpeaker02', regtype='_VirtualSpeaker._udp', port=3333)


