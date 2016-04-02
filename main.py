#!/usr/bin/env python2
from tornado import gen
from tornado.tcpclient import TCPClient
from tornado.ioloop import IOLoop
from concurrent.futures import ThreadPoolExecutor

from laterndriver import LanternDriver
from laterncontroller import LaternController
from tlvclient import TLVClient

@gen.coroutine
def start_app():
  tcpClient = TCPClient()
  try:
    stream = yield tcpClient.connect('127.0.0.1', 9999)
    print 'Connection started'
    app = LaternController(LanternDriver())
    client = TLVClient(stream)
    executer = ThreadPoolExecutor(max_workers=5)
    while True:
      command = yield client.getCommand()
      executer.submit(app.handle, command)
  except Exception as e:
    print 'Caught Error: %s' % e
    IOLoop.instance().add_callback(IOLoop.instance().stop)

if __name__ == '__main__':
  print 'App started'
  start_app()
  IOLoop.instance().start()
  IOLoop.instance().close()

