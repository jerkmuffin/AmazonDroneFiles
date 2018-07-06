#!/usr/bin/env python3

from omxplayer import OMXPlayer
import datetime
import time


print("before: {}".format(datetime.datetime.now().isoformat()))
player = OMXPlayer("takeOff.mp4")
print("after: {}".format(datetime.datetime.now().isoformat()))
try:
  while player.is_playing():
    time.sleep(0.1)
except:
  print("not playing")
print("files done: {}".format(datetime.datetime.now().isoformat()))
player.load("cruiseLoop.mp4")

