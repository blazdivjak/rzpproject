__author__ = 'gregor'

import pygame

class MyMidiObject():
    """
    Class for sending midi commands over Ethernet
    """
    # ID number of instrument
    instrument = 0
    # channel
    channel = 0
    # velocity
    velocity = 127
    # Number of playable keys
    keysNum = 127
    # List of pressed keys
    keysPressed = [False for _ in range(keysNum)]

    ''' initialziation '''
    def __init__(self, instrument, channel=0, velocity=127, keysNum = 127):
        self.instrument = instrument
        self.keysNum = keysNum
        self.channel = channel
        self.velocity = velocity

    ''' returns list of all keys status '''
    def getKeys(self):
        return self.keysPressed

    ''' set all keys at once '''
    def setKeys(self, newPressedKeys):
        if len(newPressedKeys) == self.keysNum and all(isinstance(x, bool) for x in newPressedKeys):
            self.keysPressed = newPressedKeys
        else:
            return False

    ''' change key_id status from False to True and vice versa '''
    def changeKey(self, key_id):
        if key_id < self.keysNum:
            self.keysPressed[key_id] != self.keysPressed[key_id]
            return True
        else:
            return False

    ''' returns instrument id (int) '''
    def getInstrument(self):
        return self.instrument

    ''' getters and setters '''
    def setInstrument(self, instrument):
        self.instrument = instrument

    def setChannel(self, channel):
        self.channel = channel

    def getChannel(self):
        return self.channel

    def getInstrument(self):
        return self.instrument
