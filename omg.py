#!/usr/bin/env python3

from omxplayer import OMXPlayer
import time

class foo(OMXPlayer):
  def __init__(self, file):
    self.file = file
    self.player = OMXPlayer('black.mp4')
    #self.player.pause()

  def play(self):
    self.player.play()

  def load(self):
    self.player.load(self.file)
    #self.player.pause()




foopy = OMXPlayer("takeOff.mp4")
"""try:
  while foopy.is_playing():
    time.sleep(0.1)
except:
  print("done")
finally:
  foopy.load("cruiseLoop.mp4")
"""
time.sleep(8)
foopy.load("cruiseLoop.mp4")
