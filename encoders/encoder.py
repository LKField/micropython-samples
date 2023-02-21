# encoder.py

# Copyright (c) 2016-2021 Peter Hinch
# Released under the MIT License (MIT) - see LICENSE file
# Fork edits made by Lucretia Field

from machine import Pin
from time import sleep

class Encoder:
    """Class to read and return value of rotary encoder

    :param pin_x: One of either encoder pins
    :param pin_y: Second encoder pin
    :param reverse: True/False indicator reversing encoder spin direction
    :param scale: Optional scale factor for clicks to output. Default=1
    """
    def __init__(self, pin_x, pin_y, reverse, scale=4):
        self.reverse = reverse
        self.scale = scale
        self.forward = True
        self.pin_x = pin_x
        self.pin_y = pin_y
        self._pos = 0
        try:
            self.x_interrupt = pin_x.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.x_callback, hard=True)
            self.y_interrupt = pin_y.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.y_callback, hard=True)
        except TypeError:
            self.x_interrupt = pin_x.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.x_callback)
            self.y_interrupt = pin_y.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.y_callback)
            raise
    
    def x_callback(self, line):
        self.forward = self.pin_x.value() ^ self.pin_y.value() ^ self.reverse
        self._pos += 1 if self.forward else -1

    def y_callback(self, line):
        self.forward = self.pin_x.value() ^ self.pin_y.value() ^ self.reverse ^ 1
        self._pos += 1 if self.forward else -1

    def position(self, value=None):
        if value is not None:
            self._pos = value * self.scale
        return self._pos // self.scale

    def reset(self):
        self._pos = 0

    def value(self, value=None):
        if value is not None:
            self._pos = value
        return self._pos
    
    def handler(self, min_t=1, max_t=99):
        """Reads encoder value and sets limits

        :param min_t: Minimum encoder value. Default 1 
        :param max_t: Maximum encoder value. Default 99
        :return pos_old: New 'previous' position of encoder 
        """
#         position = self.value()      # does not include SCALE factor 
        position = self.position() # includes SCALE factor 
#         position = round(position/4)
        if position < (min_t):    # below min condition
#             self._pos = 1*self.scale
            print("Min value reached")
            position = min_t
            self.position(max_t) 
#             position = self.position
        elif position > (max_t): # above max condition
#             self._pos = 99*self.scale
            position = max_t
            self.position(min_t)
#             position = self.position
            print("Max value reached") 
        return position

if __name__ == "__main__":
    phase = Pin(26, Pin.IN, Pin.PULL_UP)  # Change the 1st arg to match hardware
    quad = Pin(27, Pin.IN, Pin.PULL_UP)
    
    e = Encoder(phase, quad, False)
    print("Here!")
    count = 0
    position = e.handler(1)
    while True:
        position = e.handler()
        print("Posiiton ", position)
        sleep(0.1)

