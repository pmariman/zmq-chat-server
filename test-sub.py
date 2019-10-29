import sys
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect ("tcp://172.17.0.3:5555")

topicfilter = b"test:"
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

while True:
    string = socket.recv()
    string = string.decode('utf-8')
    topic, msg = string.split(sep=':')
    print("recv: {}:{}".format(topic, msg))
