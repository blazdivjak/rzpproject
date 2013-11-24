'''
Created on Nov 24, 2013

@author: gregor
'''
from serial import *
from threading import Thread

last_received = ''

def receiving(ser):
    while True:
        print ser.readline()

if __name__ ==  '__main__':
    #ser = Serial(port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=0.1, xonxoff=0, rtscts=0, interCharTimeout=None )
    ser = Serial('/dev/ttyACM1', 9600)

    Thread(target=receiving, args=(ser,)).start()

