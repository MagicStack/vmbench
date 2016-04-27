import argparse
import asyncio
import aiohttp
import aiohttp.server
from aiohttp import web
import sys

import uvloop

from socket import *


PRINT = 0


class HttpRequest:
    __slots__ = ('_protocol', '_url', '_headers', '_version')

    def __init__(self, protocol, url, headers, version):
        self._protocol = protocol
        self._url = url
        self._headers = headers
        self._version = version


class HttpResponse:
    __slots__ = ('_protocol', '_request', '_headers_sent')

    def __init__(self, protocol, request):
        self._protocol = protocol
        self._request = request
        self._headers_sent = False

    def write(self, data):
        if isinstance(data, str):
            data = data.encode()

        self._protocol._transport.writelines([
            'HTTP/{} 200 OK\r\n'.format(
                self._request._version).encode('latin-1'),
            b'Content-Type: text/plain\r\n',
            'Content-Length: {}\r\n'.format(len(data)).encode('latin-1'),
            b'\r\n',
            data
        ])


RESP = b'Hello World' * 512


class HttpProtocol(asyncio.Protocol):

    __slots__ = ('_loop',
                 '_transport', '_current_request', '_current_parser',
                 '_current_url', '_current_headers')

    def __init__(self, *, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._transport = None
        self._current_request = None
        self._current_parser = None
        self._current_url = None
        self._current_headers = None

    def on_url(self, url):
        self._current_url = url

    def on_header(self, name, value):
        self._current_headers.append((name, value))

    def on_headers_complete(self):
        self._current_request = HttpRequest(
            self, self._current_url, self._current_headers,
            self._current_parser.get_http_version())

        self._loop.call_soon(
            self.handle, self._current_request,
            HttpResponse(self, self._current_request))

    ####

    def connection_made(self, transport):
        self._transport = transport

    def connection_lost(self, exc):
        self._current_request = self._current_parser = None

    def data_received(self, data):
        if self._current_parser is None:
            assert self._current_request is None
            self._current_headers = []
            self._current_parser = httptools.HttpRequestParser(self)

        self._current_parser.feed_data(data)

    def handle(self, request, response):
        response.write(RESP)


def abort(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def aiohttp_server(loop, addr):
    PAYLOAD = b'<h1>Hello, World!</h1>'

    async def handle(request):
        return web.Response(body=PAYLOAD)

    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', handle)
    handler = app.make_handler()
    server = loop.create_server(handler, *addr)

    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='asyncio+aiohttp', action='store')
    parser.add_argument('--addr', default='127.0.0.1:25000', type=str)
    args = parser.parse_args()

    if args.type:
        parts = args.type.split('+')
        if len(parts) > 1:
            loop_type = parts[0]
            server_type = parts[1]
        else:
            server_type = args.type

        if server_type == 'aiohttp':
            if not loop_type:
                loop_type = 'asyncio'
        else:
            loop_type = None

        if loop_type not in {'asyncio', 'uvloop'}:
            abort('unrecognized loop type: {}'.format(loop_type))

        if server_type not in {'aiohttp', 'httptools'}:
            abort('unrecognized server type: {}'.format(server_type))

        if loop_type:
            loop = globals()[loop_type].new_event_loop()
        else:
            loop = None

        print('using {} loop: {!r}'.format(loop_type, loop))
        print('using {} HTTP server'.format(server_type))

    if loop:
        asyncio.set_event_loop(loop)
        loop.set_debug(False)

    unix = False
    if args.addr.startswith('file:'):
        unix = True
        addr = args.addr[5:]
    else:
        addr = args.addr.split(':')
        addr[1] = int(addr[1])
        addr = tuple(addr)

    server_factory = globals()['{}_server'.format(server_type)]

    print('serving on: {}'.format(addr))

    if loop:
        server = loop.run_until_complete(server_factory(loop, addr))
        try:
            loop.run_forever()
        finally:
            server.close()
            loop.close()
