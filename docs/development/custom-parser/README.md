# Custom Parser <!-- {docsify-ignore} -->

One of `fromconfig`'s strength is its flexibility when it comes to the config syntax.

To reduce the config boilerplate, it is possible to add a new `Parser` to support a new syntax.

Let's cover a dummy example : let's say we want to replace all empty strings with "lorem ipsum".

[lorem_ipsum.py](lorem_ipsum.py ':include :type=code python')
