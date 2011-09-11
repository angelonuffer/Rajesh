from twisted.internet import reactor
from twisted.web.static import File
from txWebSocket.websocket import WebSocketHandler, WebSocketSite


class Application(WebSocketHandler):

    def connectionMade(self):
        self.begin()


class ApplicationError(Exception):
    pass


def run(port=8080):
    applications = Application.__subclasses__()
    if len(applications) != 1:
        raise ApplicationError("You may have only one application")
    root = File(".")
    site = WebSocketSite(root)
    site.addHandler("/application_handler", applications[0])
    reactor.listenTCP(port, site)
    reactor.run()
