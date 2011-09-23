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

You can set python methods to javascript events::

    >>> class MyApplication(rajesh.Application):
    ...     def begin(self):
    ...         button = self.new_button("button1", "click me")
    ...         button.js.onclick = self.on_click
    ...     def on_click(self):
    ...         self.js.document.write("button clicked")

    >>> start_rajesh([MyApplication])
    >>> browser.visit("http://localhost:8080")
    >>> browser.is_text_not_present("button clicked")
    True
    >>> browser.find_by_id("button1").first.click()
    >>> browser.is_text_present("button clicked")
    True
    >>> stop_rajesh()

You can set html parameters in widget::

    >>> class MyApplication(rajesh.Application):
    ...     def begin(self):
    ...         self.new_button("button1", "button 1", onclick=self.on_click)
    ...     def on_click(self):
    ...         button2 = self.new_button("button2", "button 2")
    ...         button2["class"] = "button_class"

    >>> start_rajesh([MyApplication])
    >>> browser.visit("http://localhost:8080")
    >>> browser.is_element_not_present_by_css("button[class=button_class]")
    True
    >>> browser.find_by_id("button1").first.click()
    >>> browser.is_element_present_by_css("button[class=button_class]")
    True
    >>> stop_rajesh()
