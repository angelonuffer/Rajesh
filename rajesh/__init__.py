from twisted.internet import reactor
from twisted.web.static import File
from txWebSocket.websocket import WebSocketHandler, WebSocketSite


class JavaScript(object):

    def __init__(self, write):
        self._write = write
        self._command = ""

    def __getattr__(self, name):
        if self._command:
            self._command += ".%s" % name
        else:
            self._command = name
        return self

    def __call__(self, *args):
        self._write("%s(%s)" % (self._command, ", ".join(map(repr, args))))
        self._command = ""


class Application(WebSocketHandler):

    def connectionMade(self):
        self.js = JavaScript(self.transport.write)
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
