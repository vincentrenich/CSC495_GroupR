import argparse
import sys
import socket, threading
from nettools import *

def cmdline():
    parser = argparse.ArgumentParser(description='Game client')
    parser.add_argument('hostname', help='server host name')
    parser.add_argument('port', nargs='?', type=int, default=2222, help='server port number')
    return parser.parse_args()

class Listener(CommThread):
    def __init__(self, sock):
        super().__init__(sock)

    def run(self):
        global running
        msg = self.receive()
        while msg:
            msgQueue.enqueue(msg)
            msg = self.receive()
        if running:
            running = False
            msgQueue.enqueue('Server connection lost. Press ENTER to exit.')

def controllerMain():
    while running:
        msgQueue.waitForEvent()
        while msgQueue.notEmpty():
            print(msgQueue.dequeue())

if __name__ == "__main__":
    args = cmdline()
    controller = threading.Thread(target=controllerMain)
    controller.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.hostname, args.port))
    listener = Listener(sock)
    listener.start()
    for line in sys.stdin:
        if not running:
            break
        if len(line) > 0 and line[-1] == '\n':
            line = line[:-1]
        if line == 'exit':
            break
        listener.send(line)
    if running:
        running = False
        msgQueue.setEvent()
        sock.shutdown(socket.SHUT_WR)

# vim: set filetype=python ts=4 sw=4 expandtab:
