import new
from twisted.internet import reactor
from twisted.web.static import File
from txWebSocket.websocket import WebSocketHandler, WebSocketSite


class JavaScriptCode(object):

    def __init__(self, write):
        self._write = write
        self._command = ""
        self._events = {}

    def __getattr__(self, name):
        if self._command:
            self._command += ".%s" % name
        else:
            self._command = name
        return self

    def __setattr__(self, name, value):
        if name.startswith("_"):
            self.__dict__[name] = value
        else:
            if self._command:
                self._command += "."
            self._command += name
            if type(value) is new.instancemethod:
                function_name = value.__name__
                self._events[function_name] = value
                function = Function()
                function.sock.send(function_name)
                self._command += " = %s" % repr(function)
            else:
                self._command += " = %s" % repr(value)
            self._write(self._command)
            self._command = ""

    def __call__(self, *args):
        self._write("%s(%s)" % (self._command, ", ".join(map(repr, args))))
        self._command = ""


class Function(JavaScriptCode):

    def __init__(self):
        self._command = ""
        self._lines = []

    def __repr__(self):
        return "function() { %s }" % "; ".join(self._lines)

    def _write(self, command):
        self._lines.append(command)


class Application(WebSocketHandler):

    def connectionMade(self):
        self.js = JavaScriptCode(self.transport.write)
        self.begin()

    def frameReceived(self, message):
        method = self.js._events.get(message, None)
        if callable(method):
            method()

    def put(self, element, (x, y)):
        self.js.document.write(repr(element))
        element_id = element.parameters["id"]
        getattr(self.js, element_id).style.setProperty("position", "absolute")
        getattr(self.js, element_id).style.setProperty("top", y)
        getattr(self.js, element_id).style.setProperty("left", x)


class Expression(str):

    def __repr__(self):
        return self


class ApplicationError(Exception):
    pass


def expr(expression):
    return Expression(expression)

def run(port=8080):
    applications = Application.__subclasses__()
    if len(applications) != 1:
        raise ApplicationError("You may have only one application")
    root = File(".")
    site = WebSocketSite(root)
    site.addHandler("/application_handler", applications[0])
    reactor.listenTCP(port, site)
    reactor.run()
