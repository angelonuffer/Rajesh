from thread import start_new_thread
from socket import socket


class Request(object):

    def __init__(self, data):
        first_line = data.split("\r\n")[0]
        self.method = first_line.split(" ")[0]
        self.path = first_line.split(" ")[1]
        self.http_version = first_line.split(" ")[2]
        header, self.body = data.split("\r\n\r\n")
        self.header = {}
        for line in header.split("\r\n")[1:]:
            if ": " in line:
                key, value = line.split(": ")
                self.header[key] = value


class Response(object):

    def __init__(self, version, status, reason):
        self.http_version = version
        self.status = status
        self.reason = reason
        self.header = {}
        self.body = ""

    def __str__(self):
        first_line = " ".join([self.http_version, str(self.status), self.reason])
        header = "\r\n".join(map(lambda item: "%s: %s" % item, self.header.items()))
        return "%s\r\n%s\r\n\r\n%s" % (first_line, header, self.body)


class Client(object):

    def __init__(self, sock, (ip, port)):
        self.sock = sock
        self.ip = ip
        self.port = port

    def handle_request(self, site):
        self.request = Request(self.sock.recv(5 * (1024 ** 2)))
        handler = site.handlers.get(self.request.path, None)
        if handler is not None:
            response = handler.get_response(self)
            self.sock.send(str(response))
        self.sock.close()


class Site(object):

    def __init__(self, port):
        self.port = port
        self.sock = None
        self.handlers = {}
        self.running = False

    def run(self):
        self.sock = socket()
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(1000)
        self.running = True
        print "Server running."
        while self.running:
            client = Client(*self.sock.accept())
            start_new_thread(client.handle_request, (self,))
