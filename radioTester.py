import RPi.GPIO as g
from pygame import mixer as m
import time



g.setmode(g.BOARD)
g.setup(26, g.OUT)
g.output(26, 1)


m.init()
m.music.load('sixniner.mp3')


g.output(26, 0)
m.music.play(loops=-1)
time.sleep(30)
m.music.stop()
g.output(26, 1)
g.cleanup()
