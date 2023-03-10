#!/usr/bin/env python3

"""Instruct an AVM FRITZ!Box via UPnP_ to reconnect.

This is usually realized with tools like Netcat_ or cURL_.  However, when
developing in Python_ anyway, it is more convenient to integrate a native
implementation.  This one requires Python_ 2.5 or higher.

UPnP_ (Universal Plug and Play) control messages are based on SOAP_, which is
itself based on XML_, and transmitted over HTTP_.

Make sure UPnP_ is enabled on the FRITZ!Box.

A reconnect only takes a few second while restarting the box takes about up to
a minute; not counting the time needed to navigate through the web interface.

.. _Netcat: http://netcat.sourceforge.net/
.. _cURL:   http://curl.haxx.se/
.. _Python: http://www.python.org/
.. _UPnP:   http://www.upnp.org/
.. _SOAP:   http://www.w3.org/TR/soap/
.. _XML:    http://www.w3.org/XML/
.. _HTTP:   http://tools.ietf.org/html/rfc2616

:Copyright: 2008-2015, 2023 Jochen Kupperschmidt
:Date: 07-Feb-2023
:License: MIT
"""

import argparse
from contextlib import closing
import socket


DEFAULT_HOST = 'fritz.box'
DEFAULT_PORT = 49000

URL_PATH = '/igdupnp/control/WANIPConn1'


def reconnect(host, port, debug=False):
    """Connect to the box and submit SOAP data via HTTP."""
    request_data = create_http_request(host, port)

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.connect((host, port))
        s.send(request_data.encode('utf-8'))
        if debug:
            data = s.recv(1024)
            print('Received:', data)


def create_http_request(host, port):
    body = create_http_body()

    return '\r\n'.join(
        [
            f'POST {URL_PATH} HTTP/1.1',
            f'Host: {host}:{port:d}',
            'SoapAction: urn:schemas-upnp-org:service:WANIPConnection:1#ForceTermination',
            'Content-Type: text/xml; charset="utf-8"',
            f'Content-Length: {len(body):d}',
            '',
            body,
        ]
    )


def create_http_body():
    return '\r\n'.join(
        [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">',
            '  <s:Body>',
            '    <u:ForceTermination xmlns:u="urn:schemas-upnp-org:service:WANIPConnection:1"/>',
            '  </s:Body>',
            '</s:Envelope>',
        ]
    )


def parse_args():
    """Setup and apply the command line arguments parser."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--host',
        dest='host',
        default=DEFAULT_HOST,
        help=f'the host to send the HTTP request to [default: {DEFAULT_HOST}]',
        metavar='HOST',
    )

    parser.add_argument(
        '--port',
        dest='port',
        type=int,
        default=DEFAULT_PORT,
        help=f'the port to send the HTTP request to [default: {DEFAULT_PORT:d}]',
        metavar='PORT',
    )

    parser.add_argument(
        '--debug', dest='debug', action='store_true', default=False, help='debug mode'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    reconnect(host=args.host, port=args.port, debug=args.debug)
