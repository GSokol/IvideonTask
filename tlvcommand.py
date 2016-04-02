#!/usr/bin/env python2

class TLVCommand(object):
  _type = None
  _length = None
  _value = None

  def setType(self, input_type):
    self._type = input_type

  def getType(self):
    return self._type

  def setLength(self, length):
    self._length = length

  def getLength(self):
    return self._length

  def setValue(self, value):
    self._value = value

  def getValue(self):
    return self._value

