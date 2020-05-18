import threading
from hardware import HardWare

class TimerThread(HardWare):

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.t = threading.Thread(target=pressureControl, args={mainFrame}, kwargs={})
        self.t.start()

    