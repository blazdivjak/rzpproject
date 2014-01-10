import serial
#sudo apt-get install python-serial

#Blaz's MBP
#ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
#Gregor's HP and RaspberryPi
ser = serial.Serial('/dev/ttyACM0', 9600)
while True:
	#print ser.readline()
    line = ser.readline()
    line = line.split('\t')
    print line[0], "ms ",
    for i in line[1:]:
        #if int(i) > 300:
        #    print 1,'\t',
        #else:
        #    print 0,'\t',
        print i, '\t',
    print
