import threading
import sys
sys.path.insert(1,'../utils')
import queue

msgQueue = queue.Queue()
running = True

class CommThread(threading.Thread):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def receive(self):
        msg = ''
        pkt = self.sock.recv(2048)
        while pkt != b'':
            msg += str(pkt, encoding='utf-8')
            if msg[-1] == '\n':
                return msg[:-1]
            pkt = self.sock.recv(2048)
        self.sock.close()

    def send(self, msg):
        msg = msg + '\n'
        charssent = 0
        while charssent < len(msg):
            try:
                sent = self.sock.send(msg[charssent:].encode(encoding='utf-8'))
            except (BrokenPipeError, OSError):
                sent = 0
            if sent == 0:
                return
            charssent += sent

# vim: set filetype=python ts=4 sw=4 expandtab:
