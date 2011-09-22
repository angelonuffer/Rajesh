Widgets
=======

Widgets in rajesh are html elements, but they are dynamic.
You can put widgets on your applications::

    >>> class MyApplication(rajesh.Application):
    ...     def begin(self):
    ...         self.new_image("img1", "path_to_image")

    >>> start_rajesh([MyApplication])
    >>> browser.visit("http://localhost:8080")
    >>> browser.is_element_present_by_css("img[src=path_to_image]")
    True
    >>> stop_rajesh()

You can run javascript code in widgets with js attribute::

    >>> class MyApplication(rajesh.Application):
    ...     def begin(self):
    ...         box = self.new_box("box")
    ...         box.js.innerHTML = "text in a box"

    >>> start_rajesh([MyApplication])
    >>> browser.visit("http://localhost:8080")
    >>> browser.is_text_present("text in a box")
    True
    >>> stop_rajesh()
