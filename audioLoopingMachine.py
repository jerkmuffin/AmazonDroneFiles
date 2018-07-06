import time
import multiprocessing as mp
from omxplayer.player import OMXPlayer as omx

mp3 = "sixniner.mp3"
print('playing')
player = omx(mp3)
print('played')

#
# from pygame import mixer as m
#
# m.init()
# m.music.load("sixniner.mp3")
# m.music.play()
#
# m.music.play(loops=-1)
# m.music.stop()
