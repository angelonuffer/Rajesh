class Element(object):

    def __init__(self, name, **kwargs):
        self.name = name
        self.parameters = kwargs
        self.text = ""

    def __repr__(self):
        name = self.name
        parameters = " ".join(["%s=\"%s\"" % item for item in self.parameters.items()])
        text = self.text
        return "<%(name)s %(parameters)s>%(text)s</%(name)s>" % locals()

    def on_put(self):
        pass


class Body(Element):

    def __init__(self, **kwargs):
        super(Body, self).__init__("body", **kwargs)


class Button(Element):

    def __init__(self, **kwargs):
        super(Button, self).__init__("button", **kwargs)


class Img(Element):

    def __init__(self, **kwargs):
        super(Img, self).__init__("img", **kwargs)


class Div(Element):

    def __init__(self, **kwargs):
        super(Div, self).__init__("div", **kwargs)

    def put(self, element):
        self.text += repr(element)


class Input(Element):

    def __init__(self, **kwargs):
        super(Input, self).__init__("input", **kwargs)


class P(Element):

    def __init__(self, **kwargs):
        super(P, self).__init__("p", **kwargs)
