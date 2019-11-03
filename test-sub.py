import sys
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect('tcp://127.0.0.1:5555')

topicfilter = b"chat"
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

while True:
    string = socket.recv()
    string = string.decode('utf-8')
    chat, topic, msg = string.split(sep='/')
    print("recv: {}:{}".format(topic, msg))
