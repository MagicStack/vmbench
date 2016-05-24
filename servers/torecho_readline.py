from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer


class StreamHandler:
    def __init__(self, stream):
        self._stream = stream
        stream.set_nodelay(True)
        self._stream.read_until(b'\n', self._handle_read)

    def _handle_read(self, data):
        self._stream.write(data)
        self._stream.read_until(b'\n', self._handle_read)


class EchoServer(TCPServer):
    def handle_stream(self, stream, address):
        StreamHandler(stream)


if __name__ == '__main__':
    server = EchoServer()
    server.bind(25000)
    server.start(1)
    IOLoop.instance().start()
    IOLoop.instance().close()
