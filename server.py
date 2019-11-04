#!/usr/bin/env python3

import argparse
import http.server
import time
import threading
import zmq


# constants
HTTP_PORT=8090
RADIO_PORT=12345
PUB_PORT=5555
REP_PORT=5556


#######################################################################################################################


# TODO create server class that contains users, sessions, ...
# TODO capture exit signals


#######################################################################################################################


req_help_str = \
"""
[? | help]                      --> <this help string>
ctrl/info                       --> ctrl/users=<users>,...
ctrl/ping                       --> ctrl/ping
chat/login/<user>:<passwd>      --> chat/[ok|nok]
chat/logout/<user>              --> chat/[ok|nok]
chat/post/<topic>:<msg>         --> chat/[ok|nok]
chat/send/<user>:<msg>          --> chat/[ok|nok]"""


class replier:
    def __init__(self, zctx, port):
        self.zctx = zctx
        self.port = port
        self.open_socket()

    def open_socket(self):
        self.socket = self.zctx.socket(zmq.REP)
        self.socket.bind('tcp://0.0.0.0:{}'.format(self.port))

    def send_reply(self, rep_str):
        raw = rep_str.encode('utf-8')
        self.socket.send(raw)

    def wait_for_request(self):
        raw = self.socket.recv()
        return raw.decode('utf-8')

    def mode_chat_parse(self, req_list):
        req = req_list[1]

        if len(req) <= 1:
            rep = 'chat/nok'
            print('error: REQ [mode = chat, req = {}]'.format(req))
            return rep

        print('mode = chat, req = {}'.format(req))

        if req == 'login':
            rep = 'chat/ok'
        else:
            rep = 'chat/nok'

        return rep

    def mode_ctrl_parse(self, req_list):
        req = req_list[1]
        if len(req) <= 1:
            rep = 'ctrl/nok'
            print('error: REQ format [mode = ctrl, req = {}]'.format(req))
            return rep

        print('mode = ctrl, req = {}'.format(req))

        if req == 'info':
            rep = 'ctrl/ok'
        elif req == 'ping':
            rep = 'ctrl/pong'
        else:
            rep = 'ctrl/nok'

        return rep

    def parse_request(self, req_str):
        print('recv: {}'.format(req_str))

        if req_str in ('?', 'help'):
            rep_str = req_help_str
            return rep_str

        req_list = req_str.split(sep='/')

        if len(req_list) < 2:
            print('error: REQ format [{}]'.format(req_str))
            return 'nok'

        mode = req_list[0]

        if len(mode) <= 1:
            print('error: REQ format [{}]'.format(req_str))
            return 'nok'

        print('mode = {}'.format(mode))

        if mode == 'ctrl':
            rep_str = self.mode_ctrl_parse(req_list)
            return rep_str

        return 'nok'

    def thread_req(self):
        while True:
            req_str = self.wait_for_request()
            rep_str = self.parse_request(req_str)
            self.send_reply(rep_str)

    def start(self):
        self.tid = threading.Thread(target=self.thread_req, daemon=True)
        self.tid.start()


#######################################################################################################################


class publisher:
    def __init__(self, zctx, port):
        self.zctx = zctx
        self.port = port
        self.open_socket()

    def open_socket(self):
        self.socket = self.zctx.socket(zmq.PUB)
        self.socket.bind('tcp://0.0.0.0:{}'.format(self.port))

    def send(self, topic, msg):
        data = "chat/{}/{}".format(topic, msg)
        self.socket.send(data.encode('utf-8'))


#######################################################################################################################


http_content = \
"""<html>
<head><title>501 Not Implemented</title></head>
<body bgcolor="white">
<center><h1>501 Not Implemented</h1></center>
<hr><center>nginx</center>
</body>
</html>
"""


class SimpleReply(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(501)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self):
        return http_content.encode("utf8")

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(self._html("POST!"))

    def log_message(self, format, *args):
        return


class dummy_http:
    def __init__(self, port):
        self.port = port

    def thread_http(self):
        server_address = ("0.0.0.0", self.port)
        print('starting httpd server on {}'.format(server_address))
        httpd = http.server.HTTPServer(server_address, SimpleReply)
        httpd.serve_forever()

    def start(self):
        self.tid = threading.Thread(target=self.thread_http, daemon=True)
        self.tid.start()


#######################################################################################################################


class timed_job:
    def __init__(self, timeout, pub):
        self.timeout = timeout
        self.pub = pub
        self.start()

    def timer_callback(self):
        self.pub.send('foo', 'bar')

    def thread_wait(self):
        while not self.event.wait(self.timeout):
            self.timer_callback()

    def start(self):
        self.event = threading.Event()
        self.tid = threading.Thread(target=self.thread_wait, daemon=True)
        self.tid.start()


#######################################################################################################################


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-h', '--http', dest='http_port', type=int, nargs='?', const=HTTP_PORT,
            help='enable http socket on port (default: {})'.format(HTTP_PORT))
    parser.add_argument('-p', '--pub', dest='pub_port', type=int, nargs='?', const=PUB_PORT, default=PUB_PORT,
            help='enable publish socket on port (default: {})'.format(PUB_PORT))
    parser.add_argument('-r', '--rep', dest='rep_port', type=int, nargs='?', const=REP_PORT, default=REP_PORT,
            help='enable publish socket on port (default: {})'.format(REP_PORT))

    parser.add_argument("-v", "--verbose", dest='verbose', action='store_true', help="verbose mode")
    parser.add_argument('--help', action='help', help='show this help message and exit')

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    print('args: {}'.format(args))

    if args.http_port != None:
        web_dummy = dummy_http(args.http_port)
        web_dummy.start()

    zctx = zmq.Context()

    if args.pub_port != None:
        pub = publisher(zctx, args.pub_port)
        test = timed_job(5, pub)

    if args.rep_port != None:
        rep = replier(zctx, args.rep_port)
        rep.start()

    time.sleep(99999)


if __name__ == "__main__":
    main()
