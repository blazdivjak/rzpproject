Network of VirtualDevices playing MIDI
==========

Network of VirtualSpeakers and VirtualInstruments for streaming and playing MIDI.
Project @ Faculty of Computer and Information Science in Ljubljana, 2013/2014.

FEATURES
==========
* Read keys pressed with capacity sensing on arduino
* Automatically find VirtualSpeakers advertised on local network using mDNS and DNS-SD
* Stream different MIDI instruments on local network

INSTALL on RaspberryPi (Debian Weezy)
==========

```bash
apt-get install libavahi-compat-libdnssd-dev timidity python-serial avahi-daemon
```
```bash
pip-2.7 install pybonjour pygame
```

CONFIGURATION
==========
* Configure instruments and speakers in settings.py
* MIDI Instrument codes: http://www.ccarh.org/courses/253/handout/gminstruments/
* Start SoftSynth (we recommend to check if service is already running

```bash
service timidity start
```
* configuring number of sensor pins on Arduino board
If you are familiar with Arduino boards this should be fairly easy:
- Edit parameter ```STEVILO_SENZOR_PINOV``` to appropriate value
- Add new sensor like ```CapacitiveSensor   cs_4_12 = CapacitiveSensor(4,12);``` and donst forget to check settings in setup loop.
- Modify settings in loop() - don't forget to print to serial the new value
