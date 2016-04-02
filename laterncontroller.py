#!/usr/bin/env python2
from tlvcommand import TLVCommand
import itertools, struct
from tornado import gen

class LaternController(object):

  def _log(self, message):
    print message

  def _protocolError(self, *args):
    self._log('\033[1;41mPROTOCOL ERROR: ' + ' '.join(itertools.imap(str, args)) \
            + '\33[0m')
  @gen.coroutine
  def handle(self, command):
    if (not self._routing.has_key(command.getType()) \
            or self._routing[command.getType()][0] != command.getLength()):
      self._protocolError(command)
    else:
      self._routing[command.getType()][1](command.getValue())

  def onHandler(self, data):
    self._laternDriver.turnOn()

  def offHandler(self, data):
    self._laternDriver.turnOff()

  def colorHandler(self, data):
    color = ';'.join(itertools.imap(lambda x: hex(struct.unpack('B', x)[0]), data))
    self._laternDriver.setColor(color)

  def __init__(self, laternDriver):
    self._laternDriver = laternDriver

    self._routing = {
        0x12: (0, self.onHandler,),
        0x13: (0, self.offHandler,),
        0x20: (3, self.colorHandler,),
    }

