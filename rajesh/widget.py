from element import Img, Div, P


class Widget(object):

    def __init__(self, app, element, position):
        self.app = app
        self.element = element
        self.position = position

    @property
    def js(self):
        return getattr(self.app.js, self.element.parameters["id"])


class Document(object):

    def __init__(self, app, **kwargs):
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

    def new_box(self, id, **kwargs):
        box = Box(self.app, id=id, **kwargs)
        self.append_child(box)
        return box

    def append_child(self, widget):
        self.children.append(widget)
        self.app.put(widget.element, widget.position)


class Image(Widget):

    def __init__(self, app, path, position=(0, 0), **kwargs):
        super(Image, self).__init__(app, Img(src=path, **kwargs), position)


class Background(Image):

    def __init__(self, app, path, **kwargs):
        super(Background, self).__init__(app, path, id="background", width="100%", height="100%", **kwargs)


class Box(Widget):

    def __init__(self, app, position=(0, 0), **kwargs):
        super(Box, self).__init__(app, Div(**kwargs), position)
        self.children = []

    @property
    def inner_html(self):
        "\n".join([repr(widget.element) for widget in self.children])

    def append_child(self, widget):
        self.children.append(widget)
        self.js.innerHTML = self.inner_html


class Text(Widget):

    def __init__(self, app, id, value, position=(0, 0), **kwargs):
        super(Text, self).__init__(app, P(id=id, **kwargs), position)
        self._value = value
        self.element.text = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.js.innerHTML = value
        self._value = value
