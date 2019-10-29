import sys
import zmq

help_str = \
"""
[? | help]                                          --> <this help string>
mode:ctrl/req:info                                  --> mode:ctrl/rep:users=<users>,...
mode:ctrl/req:ping                                  --> mode:ctrl/rep:ping
mode:chat/req:login/name:<name>/passwd:<passwd>     --> mode:chat/rep:[ok|nok]
mode:chat/req:logout/name:<name>                    --> mode:chat/rep:[ok|nok]
mode:chat/req:post/topic:<name>/msg:<msg>           --> mode:chat/rep:[ok|nok]
mode:chat/req:send/user:<name>/msg:<msg>            --> mode:chat/rep:[ok|nok]
"""


def mode_ctrl_parse(req_list):
    return 'ok'


zctx = zmq.Context()
socket = zctx.socket(zmq.REP)

socket.bind("tcp://127.0.0.1:5556")

while True:
    req_str = socket.recv()
    req_str = req_str.decode('utf-8')

    print('recv: {}'.format(req_str))

    if req_str in ('?', 'help'):
        rep_str = help_str.encode('utf-8')
        socket.send(rep_str)
        continue

    req_list = req_str.split(sep='/')
    _, mode = req_list[0].split(sep=':')
    print('req mode = {}'.format(mode))

    if mode == 'ctrl':
        rep_str = mode_ctrl_parse(req_list)
        rep_str = rep_str.decode('utf-8')
        socket.send(rep_str)
    else:
        socket.send(b'ok')
