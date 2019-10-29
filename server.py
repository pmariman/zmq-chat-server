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


def mode_chat_parse(req_list):
    req = req_list[1].split(sep=':')

    if req == None or len(req) <= 1:
        rep = 'mode:chat/rep:nok'
        print('error: REQ [mode = chat, req = {}]'.format(req[0]))
        return rep

    print('mode = chat, req = {}'.format(req[1]))

    if req[1] == 'login':
        rep = 'mode:chat/rep:ok'
    else:
        rep = 'mode:chat/rep:nok'

    return rep


def mode_ctrl_parse(req_list):
    req = req_list[1].split(sep=':')

    if req == None or len(req) <= 1:
        rep = 'mode:ctrl/rep:nok'
        print('error: REQ [mode = ctrl, req = {}]'.format(req[0]))
        return rep

    print('mode = ctrl, req = {}'.format(req[1]))

    if req[1] == 'info':
        rep = 'mode:ctrl/rep:ok'
    elif req[1] == 'ping':
        rep = 'mode:ctrl/rep:pong'
    else:
        rep = 'mode:ctrl/rep:nok'

    return rep


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

    if len(req_list) < 2:
        socket.send(b'nok')
        print('error: REQ [{}]'.format(req_str))
        continue

    mode = req_list[0].split(sep=':')

    if mode == None or len(mode) <= 1:
        socket.send(b'nok')
        print('error: REQ [{}]'.format(req_str))
        continue

    print('mode = {}'.format(mode[1]))

    if mode[1] == 'ctrl':
        rep_str = mode_ctrl_parse(req_list)
        rep_str = rep_str.encode('utf-8')
        socket.send(rep_str)
    else:
        socket.send(b'nok')
