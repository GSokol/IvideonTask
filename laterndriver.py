#!/usr/bin/env python2

import time

class LanternDriver(object):
  _TURN_ON_MESSAGE = 'Latern is turned on%s'
  _TURN_OFF_MESSAGE = 'Latern is turned off%s'
  _SET_COLOR_MESSAGE = 'Latern\'s color is swiched to %s.'

  _COLOR_PREFIX = ', color is %s.'

  def _log(self, message):
    print '\033[1;92m' + message + '\033[0m'

  def turnOn(self):
    time.sleep(10)
    self._log(self._TURN_ON_MESSAGE % (self._COLOR_PREFIX % self._color \
            if self._color else '.'))

  def turnOff(self):
    time.sleep(10)
    self._log(self._TURN_OFF_MESSAGE % (self._COLOR_PREFIX % self._color \
            if self._color else '.'))

  def setColor(self, color):
    time.sleep(10)
    self._color = color
    self._log(self._SET_COLOR_MESSAGE % color)

  def __init__(self):
    self._color = None

