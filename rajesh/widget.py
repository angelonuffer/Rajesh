from element import Body, Img


class Widget(object):

    def __init__(self, app, element):
        self.app = app
        self.element = element


class Document(Widget):

    def __init__(self, app, **kwargs):
        super(Document, self).__init__(app, Body(**kwargs))
        self._background = ""

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value):
        self._background = Background(self.app, value)


class Image(Widget):

    def __init__(self, app, path, position=(0, 0), **kwargs):
        super(Image, self).__init__(app, Img(src=path, **kwargs))
        self.app.put(self.element, position)


class Background(Image):

    def __init__(self, app, path, **kwargs):
        super(Background, self).__init__(app, path, id="background", width="100%", height="100%", **kwargs)
