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

    def get_response(self, client):
        connection = client.request.header.get("Connection", "")
        upgrade = client.request.header.get("Upgrade", "")
        if connection == "Upgrade":
            if upgrade.lower() == "websocket":
                self.process_websocket_request(client)

    def process_websocket_request(self, client):
        sec_key_1 = client.request.header.get("Sec-WebSocket-Key1", "")
        sec_key_2 = client.request.header.get("Sec-WebSocket-Key2", "")
        origin = client.request.header.get("Origin", "")
