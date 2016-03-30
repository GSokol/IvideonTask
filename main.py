#!/usr/bin/env python2
import itertools
from operator import add
from tornado import gen
from tornado.tcpclient import TCPClient
from tornado.ioloop import IOLoop

class LanternDriver(object):
  _TURN_ON_MESSAGE = 'Latern is turned on%s'
  _TURN_OFF_MESSAGE = 'Latern is turned off%s'
  _SET_COLOR_MESSAGE = 'Latern\'s color is swiched to %s.'

  _COLOR_PREFIX = ', color is %s.'

  def _log(self, message):
    print '\033[1;92m' + message + '\033[0m'

  def turnOn(self):
    self._log(self._TURN_ON_MESSAGE % (self._COLOR_PREFIX % self._color \
            if self._color else '.'))

  def turnOff(self):
    self._log(self._TURN_OFF_MESSAGE % (self._COLOR_PREFIX % self._color \
            if self._color else '.'))

  def setColor(self, color):
    self._color = color
    self._log(self._SET_COLOR_MESSAGE % color)

  def __init__(self):
    self._color = None

class Application(object):

  def _bigEndianDecode(self, data):
    return reduce(add, itertools.imap(lambda i: ord(data[i]) * (256 ** (len(data) - i - 1)), xrange(len(data))))

  def _log(self, message):
    print message

  def _protocolError(self, commandLength, *args):
    self._log('\033[1;41mPROTOCOL ERROR: ' + ' '.join(itertools.imap(str, args)) \
            + '\033[0m')
    self._stream.read_bytes(commandLength)

  def _readCommand(self):
    self._stream.read_bytes(3, self.dispatch)

  def dispatch(self, data):
    print data
    commandType = self._bigEndianDecode(data[0:1])
    commandLength = self._bigEndianDecode(data[1:3])

    if (not self._routing.has_key(commandType)):
      self._protocolError(commandLength, commandType)
      self._readCommand()
      return

    route = self._routing[commandType]
    if (route[0] != commandLength):
      self._protocolError(commandLength, commandType, commandLength)
      self._readCommand()
      return

    self._stream.read_bytes(commandLength, route[1])

  def onHandler(self, data):
    self._laternDriver.turnOn()
    self._readCommand()

  def offHandler(self, data):
    self._laternDriver.turnOff()
    self._readCommand()

  def colorHandler(self, data):
    color = ';'.join(itertools.imap(hex, (self._bigEndianDecode(data[0:1]), \
            self._bigEndianDecode(data[1:2]), \
            self._bigEndianDecode(data[2:3]))))
    self._laternDriver.setColor(color)

  def __init__(self, stream, laternDriver):
    self._stream = stream
    self._laternDriver = laternDriver

    self._routing = {
        0x12: (0, self.onHandler,),
        0x13: (0, self.offHandler,),
        0x20: (3, self.colorHandler,),
    }


  def run(self):
    self._readCommand()

@gen.coroutine
def start_app():
  driver = LanternDriver()
  tcpClient = TCPClient()
  try:
    stream = yield tcpClient.connect('127.0.0.1', 9999)
    print 'Connection started'
    app = Application(stream, driver)
    app.run()
  except Exception as e:
    print 'Caught Error: %s' % e
    IOLoop.instance().add_callback(IOLoop.instance().stop)

if __name__ == '__main__':
  start_app()
  IOLoop.instance().start()
  IOLoop.instance().close()

