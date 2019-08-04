import asyncio
import logging
import threading
import queue

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer


class ControlServer(TCPServer):
    """
    This is a simple TCP Server
    """
    message_separator = b'\r\n'

    def __init__(self, *args, **kwargs):
        self._connections = []
        self.logger = logging.getLogger('ControlServer')
        self.logger.debug('__init__')

        self.receive_queue = queue.Queue(1)
        super(ControlServer, self).__init__(*args, **kwargs)

    def set_receive_q(self, receive_q: queue.Queue):
        self.receive_queue = receive_q

    @gen.coroutine
    def handle_stream(self, stream, address):
        """
        Main connection loop. Launches listen on given channel and keeps
        reading data from socket until it is closed.
        """
        try:
            self.logger.info('New request has come from our {} buddy...'.format(address))
            while True:
                try:
                    request = yield stream.read_until(self.message_separator)
                    self.logger.info("received request")
                    self.logger.info(request)
                    self.receive_queue.put_nowait(request)
                except StreamClosedError as e:
                    self.logger.error("stream error: {}".format(e))
                    stream.close(exc_info=True)
                    return
                except queue.Full:
                    continue
        except Exception as e:
            if not isinstance(e, gen.Return):
                self.logger.error("Connection loop has experienced an error.")


class ControlServerThread(threading.Thread):

    def __init__(self, port, receive_q: queue.Queue):
        threading.Thread.__init__(self)
        self.port = port
        self.logger = logging.getLogger('ControlServerThread')
        self.logger.debug('__init__')
        self.server = ControlServer()
        self.server.set_receive_q(receive_q)

    def __del__(self):
        self.stop_server()

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.server.listen(self.port)
        self.logger.info("Starting the control server")
        IOLoop.instance().start()
        self.logger.info('Server has shut down.')

    def stop_server(self):
        self.server.stop()
