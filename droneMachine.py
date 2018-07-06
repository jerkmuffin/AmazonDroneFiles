#!/usr/bin/env python2

import OSC
import time
import RPi.GPIO as g
import multiprocessing as mp

from time import sleep
from OSC import OSCServer

from pygame import mixer as m

IP = '192.168.0.8'
PORT = 8000
c = OSC.OSCClient()
c.connect((IP, PORT))

g.setmode(g.BOARD)
g.setwarnings(False)
MATRIX = [[1, 2, 3, 'A'],
          [4, 5, 6, 'B'],
          [7, 8, 9, 'C'],
          ['*', 0, '#', 'D']]


ROW = [7, 11, 13, 15]
COL = [12, 16, 18, 22]
CODE = '793'


LOCK = 37
POWER = 38
BUTTON = 40
BUTTONLIGHT = 8
RADIORELAY = 26
g.setup(POWER, g.IN, pull_up_down=g.PUD_UP)
g.setup(LOCK, g.IN, pull_up_down=g.PUD_UP)
g.setup(BUTTON, g.IN, pull_up_down=g.PUD_UP)
g.setup(RADIORELAY, g.OUT)
g.setup(BUTTONLIGHT, g.OUT)
g.output(BUTTONLIGHT, 1)
g.output(RADIORELAY, 1)

for j in range(4):
    g.setup(COL[j], g.OUT)
    g.output(COL[j], 1)

for i in range(4):
    g.setup(ROW[i], g.IN, pull_up_down=g.PUD_UP)

m.init()
m.music.load("sixniner.mp3")


def osc_set_reset(address):
    m = OSC.OSCMessage()
    m.setAddress(address)
    m.append(1)
    c.send(m)
    time.sleep(1)
    m = OSC.OSCMessage()
    m.setAddress(address)
    m.append(0)
    c.send(m)


def check(str):
    print('checking: {}'.format(str))
    if len(str) >= len(CODE):
        # print('greater: {}, {}'.format(str[-4:-1], CODE))
        if str[-len(CODE):] == CODE:
            print("you did the code!")
            osc_set_reset('/droneGame/push4')
            return True



def keypad(gameState):
    foo = ''
    while (gameState == gamePosition):
        for j in range(4):
            g.output(COL[j], 0)

            for i in range(4):
                if g.input(ROW[i]) == 0:
                    print(MATRIX[i][j])
                    if MATRIX[i][j] == 0:
                        print("ZERO!")
                        if check(foo):
                            gameState = gamePositionList[gamePositionList.index(gameState) + 1]
                    foo += str((MATRIX[i][j]))
                    while(g.input(ROW[i]) == 0):
                        pass
            g.output(COL[j], 1)

def switch_test(inputNum, gameState):
    state = ''
    newstate = state
    while (gameState == gamePosition):
        if g.input(inputNum) == 0:
            newstate = gameState+'_on'
            if state != newstate:
                state = newstate
                print('state change: {}'.format(state))
                gameState = 'X'
        else:
            newstate = gameState+'_off'
            if state != newstate:
                state = newstate
                print('state change: {}'.format(state))


class BlinkHandler(object):
    def __init__(self, section):
        pin_dict = {'power': {'green': 5, 'red': 3, 'status': 'off'},
                    'key': {'green': 24, 'red': 23, 'status': 'off'},
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
            self._off(self.ledIndicator['green'])
        elif self.ledIndicator['status'] == 'red':
            self.event.set()
            for p in self.procs:
                p.join()
            self.event.clear()

    def changeState(self, state):
        self.updatePreviousState()
        if state == 'green':
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

# end blinkHandler


foo = ''
state = ''
newState = state
pstate = ''
newPstate = pstate
gamePositionList = ['start', 'powerCabled', 'keyInserted', 'radioCalled',
                    'keypadEntered', 'buttonPushed']
gamePosition = gamePositionList[0]


powerLed = BlinkHandler('power')
keyLed = BlinkHandler('key')
numLed = BlinkHandler('numpad')
buttonLed = BlinkHandler('button')



### server ###
server = OSCServer( ("0.0.0.0", 8888) )
server.timeout = 0


def handle_timeout(self):
    self.timed_out = True

def cb(path, tags, args, source):
    if args[0] == 1:
        gamePosition = 'start'
        print('game position is now start!')
        try:
            powerLed.changeState('off')
            keyLed.changeState('off')
            numLed.changeState('off')
            buttonLed.changeState('off')
            print("reset game postion: {}".format(gamePosition))
        except Exception as e:
            print('that didna work')
            print(e)
    print(path, tags, args, source)

def nothing(*args):
    pass

server.addMsgHandler("/yes/please", cb)
server.addMsgHandler("/yes/no", nothing)

def each_frame():
    server.timed_out = False
    while not server.timed_out:
        server.handle_request()


def run():
    sleep(1)
    each_frame()

t = mp.Process(target=run, args=())
t.start()

###  end server


try:
    while True:

        if gamePosition == 'start':
            print('hello I am start')
            # powerLed = BlinkHandler('power')
            powerLed.changeState('red')
            switch_test(POWER, gamePosition)
            powerLed.changeState('green')
            osc_set_reset('/droneGame/push2')
            gamePosition = gamePositionList[1]
            print('foo: {}'.format(gamePosition))
        elif gamePosition == 'powerCabled':
            # keyLed = BlinkHandler('key')
            keyLed.changeState('red')
            switch_test(LOCK, gamePosition)
            keyLed.changeState('green')
            osc_set_reset('/droneGame/push3')
            gamePosition = gamePositionList[2]
        elif gamePosition == 'keyInserted':
            # numLed = BlinkHandler('numpad')
            numLed.changeState('red')
            print("radio?")
            g.output(RADIORELAY, 0)
            m.music.play(loops=-1)
            keypad(gamePosition)
            numLed.changeState('green')
            m.music.stop()
            g.output(RADIORELAY, 1)
            print('and then???')
            gamePosition = 'keypadEntered'

            ### deal with radio here

        elif gamePosition == 'keypadEntered':
            # buttonLed = BlinkHandler('button')
            buttonLed.changeState('red')
            g.output(BUTTONLIGHT, 0)
            print("Button status: {}".format(g.input(BUTTON)))
            switch_test(BUTTON, gamePosition)
            print("buttoned?")
            buttonLed.changeState('green')
            g.output(BUTTONLIGHT, 1)
            osc_set_reset('/droneGame/push5')
            gamePosition = 'XXX'
            print('missle launched muslims destroyed\ncongratulations you are racist!!')

except KeyboardInterrupt as e:
    osc_set_reset('/4toggles/push8')
    print("fml: {}".format(e))
    g.cleanup()
