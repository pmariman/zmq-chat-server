#!/usr/bin/env python3

import sys
import zmq

zctx = zmq.Context()
socket = zctx.socket(zmq.REQ)

socket.connect("tcp://127.0.0.1:5556")

while True:
    req_str = input('>> ')

    if len(req_str) == 0:
        continue

    req_str = req_str.encode('utf-8')
    socket.send(req_str)

    rep_str = socket.recv()
    rep_str = rep_str.decode('utf-8')
    print('recv: {}'.format(rep_str))
