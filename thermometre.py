from hardware import *


class Thermometre():
    def __init__(self, parent,bus,inPin,*args, **kwargs):
        self.parent = parent
        self.bus=bus
        self.inPin=inPin

    def getTemp(self):
        temp = self.bus.send(MODULE_ADDRESS, TMCL.commands.Command.GIO, self.inPin, 1, 0).value
        temp=0.0004485*temp+17.40575
        return round(temp,1)