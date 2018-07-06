#!/usr/bin/env python

from flask import Flask
from omxplayer import OMXPlayer

app = Flask(__name__)

@app.route('/')
def play():
  foo = OMXPlayer("takeOff.mp4")
  return True

@app.route('/test')
def test():
  foo = "testing 1 2 3...\n"
  print(foo)
  return(foo)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

