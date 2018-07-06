import multiprocessing as mp
import RPi.GPIO as g
import time


g.setmode(g.BOARD)
g.setwarnings(False)
#pairs of red and green
outlist = [3, 5, 23, 24, 31, 32, 35, 36]
for o in outlist:
    g.setup(o, g.OUT)
    g.output(o, 1)


class BlinkHandler(object):
    def __init__(self, section):
        pin_dict = {'power': {'green': 5, 'red': 3, 'status': 'off'},
                    'key': {'green': 24, 'red': 22, 'status': 'off'},
                    'numpad': {'green': 32, 'red': 31, 'status': 'off'},
                    'button': {'green': 36, 'red': 35, 'status': 'off'}}
        self.ledIndicator = pin_dict[section]
        self.procs = []
        self.event = mp.Event()
        for pin in (self.ledIndicator['green'], self.ledIndicator['red']):
            g.setup(pin, g.OUT)
            g.output(pin, 1)



    def _redBlink(self, blinkPin):
        while not self.event.is_set():
            g.output(blinkPin, 0)
            time.sleep(.25)
            g.output(blinkPin, 1)
            time.sleep(.25)

    def _soldGreen(self, blinkPin):
        g.output(blinkPin, 0)

    def _off(self, blinkPin):
        g.output(blinkPin, 1)

    def updatePreviousState(self):
        if self.ledIndicator['status'] == 'green':
            print('status: {}'.format(self.ledIndicator['status']))
            self._off(self.ledIndicator['green'])
        elif self.ledIndicator['status'] == 'red':
            print('status: {}'.format(self.ledIndicator['status']))
            self.event.set()
            for p in self.procs:
                p.join()
            self.event.clear()

    def changeState(self, state):
        self.updatePreviousState()
        if state == 'green':
            print('trying to change to green')
            self._soldGreen(self.ledIndicator['green'])
            self.ledIndicator['status'] = 'green'
        elif state == 'red':
            x = mp.Process(target=(self._redBlink), args=(self.ledIndicator['red'],))
            x.start()
            self.procs.append(x)
            self.ledIndicator['status'] = 'red'
        elif state == 'off':
            self.event.set()
            for p in self.procs:
                p.join()
            self.event.clear()
            self._off(self.ledIndicator['red'])
            self._off(self.ledIndicator['green'])





        # change to new state
        # update status


powerLed = BlinkHandler('power')

powerLed.changeState('red')

time.sleep(2)

powerLed.changeState('green')

time.sleep(2)

powerLed.changeState('red')

time.sleep(2)

powerLed.changeState('off')
