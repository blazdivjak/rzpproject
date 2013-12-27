__author__ = 'blaz'

import socket

import pybonjour

#get hostname advertised in mDNS
def getHostName(hostname):
    return socket.gethostbyname(hostname)

#######MAIN#######
print getHostName('Blazs-MacBook-Pro-2.local')