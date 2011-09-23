import new
from element import Img, Div, P
from element import Button as ButtonElement


class CSSSheet(object):

    def __init__(self, widget):
        self._widget = widget

    def __setattr__(self, property_, value):
        if property_.startswith("_"):
            self.__dict__[property_] = value
        else:
            self._widget.js.style.setProperty(property_, value)


class Widget(object):

    def __init__(self, app, id_, element):
        self.app = app
        self.id_ = id_
        self.element = element
        self.element.parameters["id"] = id_
        self.children = []
        self.css = CSSSheet(self)

    def __getitem__(self, key):
        return self.element.parameters[key]

    def __setitem__(self, key, value):
        self.js.setAttribute(key, value)
        self.element.parameters[key] = value

    @property
    def js(self):
        return getattr(self.app.js, self.id_)

    def append_child(self, widget):
        self.children.append(widget)
        self.app.put(widget.element)
        widget.on_put()

    def set_position(self, x, y):
        self.js.style.setProperty("position", "absolute")
        self.js.style.setProperty("top", y)
        self.js.style.setProperty("left", x)

    def on_put(self):
        for parameter, value in self.element.parameters.items():
            if type(value) is new.instancemethod:
                setattr(self.js, parameter, value)


class Document(Widget):

    def __init__(self, app):
        self.app = app
        self._background = ""
        self.children = []

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value):
        self._background = Background(self.app, value)
        self.append_child(self._background)


class Image(Widget):

    def __init__(self, app, id_, path, **kwargs):
        super(Image, self).__init__(app, id_, Img(src=path, **kwargs))


class Background(Image):

    def __init__(self, app, path, **kwargs):
        super(Background, self).__init__(app, "background", path, width="100%", height="100%", **kwargs)

    def on_put(self):
        super(Background, self).on_put()
        self.set_position(0, 0)


class Box(Widget):

    def __init__(self, app, id_, **kwargs):
        super(Box, self).__init__(app, id_, Div(**kwargs))


class Text(Widget):

    def __init__(self, app, id_, value, **kwargs):
        super(Text, self).__init__(app, id_, P(**kwargs))
        self._value = value
        self.element.text = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.js.innerHTML = value
        self._value = value


class Button(Widget):

    def __init__(self, app, id_, text, **kwargs):
        element = ButtonElement(**kwargs)
        element.text = text
        super(Button, self).__init__(app, id_, element)
