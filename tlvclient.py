#!/usr/bin/env python2

from tlvcommand import TLVCommand
import struct
from tornado import gen
from tornado.concurrent import TracebackFuture

class TLVClient(object):

  def __init__(self, stream):
    self._stream = stream

  @gen.coroutine
  def getCommand(self):
    command = TLVCommand()
    command_type = yield self._stream.read_bytes(1)
    command.setType(struct.unpack('B', command_type)[0])
    command_length = yield self._stream.read_bytes(2)
    command.setLength(struct.unpack('>H', command_length)[0])
    commadn_value = yield self._stream.read_bytes(command.getLength())
    command.setValue(commadn_value)
    raise gen.Return(command)

  def _getData(self, data):
    self._data = data
