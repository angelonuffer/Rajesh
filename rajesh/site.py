from thread import start_new_thread
from socket import socket


class Request(object):

    def __init__(self, data):
        first_line = data.split("\r\n")[0]
        self.method = first_line.split(" ")[0]
        self.path = first_line.split(" ")[1]
        self.http_version = first_line.split(" ")[2]
        self.header = {}
        for line in data.split("\r\n")[1:]:
            if line:
                key, value = line.split(": ")
                self.header[key] = value


class Client(object):

    def __init__(self, sock, (ip, port)):
        self.sock = sock
        self.ip = ip
        self.port = port
        self.request = Request(self.sock.recv(5 * (1024 ** 2)))
        self.sock.close()


class Site(object):

    def __init__(self, port):
        self.port = port
        self.sock = None
        self.handlers = {}

    def run(self):
        self.sock = socket()
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(1000)
        self.running = True
        while self.running:
            client = Client(*self.sock.accept())
