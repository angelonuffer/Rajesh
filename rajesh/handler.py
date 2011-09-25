import struct
from hashlib import md5
from site import Response


class Handler(object):

    def get_response(self):
        return ""


class File(Handler):

    def __init__(self, path):
        self.path = path
        self.data = open(path).read()

    def get_response(self, client):
        response = Response(client.request.http_version, 200, "OK")
        response.body = self.data
        return response


class WebSocketHandler(Handler):

    def __init__(self):
        self.running = False

    def get_response(self, client):
        connection = client.request.header.get("Connection", "")
        if connection != "Upgrade":
            return ""
        upgrade = client.request.header.get("Upgrade", "")
        if upgrade.lower() != "websocket":
            return ""
        sec_key_1 = client.request.header.get("Sec-WebSocket-Key1", "")
        sec_key_2 = client.request.header.get("Sec-WebSocket-Key2", "")
        origin = client.request.header.get("Origin", "")
        host = client.request.header.get("Host", "")
        number1 = int(filter(lambda x: x in "0123456789", sec_key_1))
        number2 = int(filter(lambda x: x in "0123456789", sec_key_2))
        number_of_spaces_1 = sec_key_1.count(" ")
        number_of_spaces_2 = sec_key_2.count(" ")
        if number_of_spaces_1 == 0 or number_of_spaces_2 == 0:
            return ""
        number1 /= number_of_spaces_1
        number2 /= number_of_spaces_2
        response = Response(client.request.http_version, 101, "Web Socket Protocol Handshake")
        response.header["Connection"] = "Upgrade"
        response.header["Upgrade"] = "WebSocket"
        response.header["Sec-WebSocket-Origin"] = origin
        response.header["Sec-WebSocket-Location"] = "ws://%s%s" % (host, client.request.path)
        response.body = md5(struct.pack(">II8s", number1, number2, client.request.body)).digest()
        client.sock.send(str(response))
        self.sock = client.sock
        self.connection_made()
        self.running = True
        self.receive_messages()

    def write(self, data):
        self.sock.send("\x00%s\xff" % data)

    def receive_messages(self):
        while self.running:
            byte = ""
            while byte != "\x00":
                byte = self.sock.recv(1)
            byte = ""
            message = ""
            while byte != "\xff":
                message += byte
                byte = self.sock.recv(1)
            self.message_received(message)
