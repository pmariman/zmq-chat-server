import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.RADIO)

socket.connect('udp://127.0.0.1:5555')

while True:
    socket.send(b'hello', group='test')
    time.sleep(5)
