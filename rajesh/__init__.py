import os
import new
import socket
from twisted.internet import reactor
from twisted.web.static import File
from txWebSocket.websocket import WebSocketHandler, WebSocketSite
from widget import Document, Image, Button, Box
from site import Site
from handler import File, WebSocketHandler


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

    def connection_made(self):
        self.js = JavaScriptCode(self.write)
        self._title = ""
        self.document = Document(self)
        self.begin()

    def message_received(self, message):
        words = message.split(" ")
        method_name = words[0]
        parameters = words[1:] if len(words) > 1 else []
        method = self.js._events.get(method_name, None)
        if callable(method):
            method(*parameters)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.js.document.title = value

    @property
    def background(self):
        return self.document.background

    @background.setter
    def background(self, value):
        self.document.background = value

    def new_box(self, id, **kwargs):
        box = Box(self, id, **kwargs)
        self.document.append_child(box)
        return box

    def new_image(self, id, path, **kwargs):
        image = Image(self, id, path, **kwargs)
        self.document.append_child(image)
        return image

    def new_button(self, id, text, **kwargs):
        button = Button(self, id, text, **kwargs)
        self.document.append_child(button)
        return button

    def put(self, element):
        self.js.document.write(repr(element))


class Expression(str):

    def __repr__(self):
        return self


class ApplicationError(Exception):
    pass


def expr(expression):
    return Expression(expression)

def run(port=8080, applications=None):
    if applications is None:
        applications = Application.__subclasses__()
    if len(applications) != 1:
        raise ApplicationError("You may have only one application")
    site = Site(port)
    site.handlers["/"] = File("index.html")
    site.handlers["/rajesh.js"] = File("rajesh.js")
    site.handlers["/application_handler"] = applications[0]()
    while not site.running:
        try:
            site.run()
        except KeyboardInterrupt:
            site.sock.close()
        except socket.error:
            pass
