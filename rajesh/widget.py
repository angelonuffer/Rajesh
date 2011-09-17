from element import Img, Div


class Widget(object):

    def __init__(self, app, element, position):
        self.app = app
        self.element = element
        self.position = position


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

    def new_box(self, id, position):
        box = Box(self.app, position, id=id)
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
