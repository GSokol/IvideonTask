#!/usr/bin/env python2

from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer

class EchoServer(TCPServer):
  def handle_stream(self, stream, address):
    print '!!!!!'
    self._stream = stream
    self._stream.write(b'\x12\x00\x00')
    self._stream.write(b'\x13\x00\x00')
    self._stream.write(b'\x20\x00\x03\xff\x00\x00')

if __name__ == '__main__':
  server = EchoServer()
  server.listen(9999)
  IOLoop.instance().start()
  IOLoop.instance().close()
