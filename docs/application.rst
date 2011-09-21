Application
===========

To create an application in rajesh, you need to have an application class like::

    >>> class MyApplication(rajesh.Application):
    ...     pass

Each request to application instances a new application object and calls the
"begin" method. You can call javascript functions with the js attribute::

    >>> class MyApplication(rajesh.Application):
    ...     def begin(self):
    ...         self.js.document.write("test application")

    >>> start_rajesh([MyApplication])
    >>> browser.visit("http://localhost:8080")
    >>> browser.is_text_present("test application")
    True
    >>> stop_rajesh()

You can set the title of application with title attribute::

    >>> class MyApplication(rajesh.Application):
    ...     def begin(self):
    ...         self.title = "My application"

    >>> start_rajesh([MyApplication])
    >>> browser.visit("http://localhost:8080")
    >>> browser.title
    u'My application'
    >>> stop_rajesh()

You can create a background.

NOTE: The background here is an img element that resizes following the browser
window::

    >>> class MyApplication(rajesh.Application):
    ...     def begin(self):
    ...         self.background = "path_to_image"

    >>> start_rajesh([MyApplication])
    >>> browser.visit("http://localhost:8080")
    >>> browser.is_element_present_by_css("img[src=path_to_image]")
    True
    >>> stop_rajesh()
