Network of VirtualDevices playing MIDI
==========

Network of VirtualSpeakers and VirtualInstruments for streaming and playing MIDI.
Project @ Faculty of Computer and Information Science in Ljubljana, 2013/2014.

FEATURES
==========
* Read keys pressed with capacity sensing on arduino
* Automaticly find VirtualSpeakers advertised on local network using mDNS and DNS-SD
* Stream different MIDI instruments on local network

INSTALL on RaspberryPi (Debian Weezy)
==========

```bash
    apt-get install libavahi-compat-libdnssd-dev timidity
```
```bash
    pip-2.7 install pybonjour pygame
```

CONFIGURATION
==========
* Configure instruments and speakers in settings.py
* MIDI Instrument codes: http://www.ccarh.org/courses/253/handout/gminstruments/

