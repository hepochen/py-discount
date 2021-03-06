Discount
========

This Python package is a `ctypes`_ binding of `David Parson`_'s
`Discount`_, a C implementation of `John Gruber`_'s `Markdown`_.

.. _`ctypes`:      http://docs.python.org/library/ctypes.html
.. _`David Parson`: http://www.pell.portland.or.us/~orc
.. _`Discount`:    http://www.pell.portland.or.us/~orc/Code/discount/
.. _`John Gruber`: http://daringfireball.net/
.. _`Markdown`:    http://daringfireball.net/projects/markdown

.. contents::


Introduction
------------

Markdown is a text-to-HTML conversion tool for web writers.  Markdown
allows you to write using an easy-to-read, easy-to-write plain text
format, then convert it to structurally valid XHTML (or HTML).

The ``discount`` Python module contains two things of interest:

* ``libmarkdown``, a submodule that provides access to the public C
  functions defined by Discount.

* ``Markdown``, a helper class built on top of ``libmarkdown``,
  providing a more familiar Pythonic interface


Using the ``Markdown`` class
----------------------------

The ``Markdown`` class wraps the C functions exposed in the
``libmarkdown`` submodule and handles the ctypes leg work for you.  If
you want to use the Discount functions directly, skip to the next
section about ``libmarkdown``.

Let's take a look at a simple example::

    import sys
    import discount

    mkd = discount.Markdown(sys.stdin)
    mkd.write_html_content(sys.stdout)


``Markdown`` takes one required argument, ``input_file_or_string``,
which is either a file object or a string-like object.

    **Note:** There are limitations to what kind of file-like objects
    can be passed to ``Markdown``.  File-like objects like
    ``StringIO`` can't be handled at the C level in the same way as OS
    file objects like ``sys.stdin`` and ``sys.stdout``, or file
    objects returned by the builtin ``open()`` method.

``Markdown`` also has methods for getting the output as a string,
instead of writing to a file-like object.  Let's look at a modified
version of the first example, this time using strings::

    import discount

    mkd = discount.Markdown('`test`')
    print mkd.get_html_content()

Currently, ``Markdown`` does not manage character encoding, since the
``Markdown`` wraps C functions that support any character encoding
that is a superset of ASCII.  However, when working with unicode
objects in Python, you will need to pass them as bytestrings to
``Markdown``, and then convert them back to unicode afterwards.  Here
is an example of how you could do this::

   import discount

   txt = u'\xeb' # a unicode character, an e with an umlaut
   mkd = discount.Markdown(txt.encode('utf-8'))
   out = mkd.get_html_content()
   val = out.decode('utf-8')

The ``Markdown`` class constructor also takes optional boolean keyword
arguments that map to Discount flags compilation flags.

``toc``
  Generate table-of-contents headers (each generated <h1>, <h2>,
  etc will include a id="name" argument.)  Use ``get_html_toc()``
  or ``write_html_toc()`` to generate the table-of-contents
  itself.

``strict``
  Disable relaxed emphasis and superscripts.

``autolink``
  Greedily expand links; if a url is encountered, convert it to a
  hyperlink even if it isn't surrounded with ``<>s``.

``safelink``
  Be paranoid about how ``[][]`` is expanded into a link - if the
  url isn't a local reference, ``http://``, ``https://``,
  ``ftp://``, or ``news://``, it will not be converted into a
  hyperlink.

``ignore_header``
  Do not process the `pandoc document header`_, but treat it like
  regular text.

``ignore_links``
  Do not allow ``<a`` or expand ``[][]`` into a link.

``ignore_images``
  Do not allow ``<img`` or expand ``![][]`` into a image.

``ignore_tables``
  Don't process `PHP Markdown Extra`_ tables.

``ignore_smartypants``
  Disable `SmartyPants`_ processing.

``ignore_embedded_html``
  Disable all embedded HTML by replacing all ``<``'s with
  ``&lt;``.

``ignore_pseudo_protocols``
  Do not process `pseudo-protocols`_.

Pandoc header elements can be retrieved with the methods
``get_pandoc_title()``, ``get_pandoc_author()`` and
``get_pandoc_date()``.

The converted HTML document parts can be retrieved as a string
with the ``get_html_css()``, ``get_html_toc()`` and
``get_html_content()`` methods, or written to a file with the
``write_html_css(fp)``, ``write_html_toc(fp)`` and
``write_html_content(fp)`` methods, where ``fp`` is the output file
descriptor.

Discount provides two hooks for manipulating links while processing
markdown.  The first lets you rewrite urls specified by ``[]()``
markup or ``<link/>`` tags, and the second lets you add additional
HTML attributes on ``<a/>`` tags generated by Discount.  You can pass
callback functions to ``Markdown``'s ``rewrite_links_func`` and
``link_attrs_func`` keyword arguments respectively.

Here is an example of a callback function that adds the domain name to
internal pages::

    def add_basepath(url):
        if url.startswith('/'):
            return 'http://example.com%s' % url

    md = Markdown(
        '`[a](/a.html)`',
        rewrite_links_func=add_basepath
    )

Here is an example that opens external pages in another window/tab::

    def add_target_blank(url):
        if url.startswith('http://'):
            return 'target="_blank"'

    md = Markdown(
        '`[a](http://example.com/a.html)`',
        link_attrs_func=add_target_blank
    )

Alternatively, you can attach these callbacks using decorators::

    md = Markdown('`[a](/a.html)`')

    @md.rewrite_links
    def add_basepath(url):
        # same as above
        ...

    md = Markdown('`[a](http://example.com/a.html)`')

    @md.link_attrs
    def add_target_blank(url):
        # same as above
        ...

Under some conditions, the functions in ``libmarkdown`` may return
integer error codes.  These errors are raised as a ``MarkdownError``
exceptions when using the ``Markdown`` class.

.. _`pandoc document header`:
     http://johnmacfarlane.net/pandoc/README.html#title-blocks
.. _`PHP Markdown Extra`:
     http://michelf.com/projects/php-markdown/extra/.
.. _`SmartyPants`:
     http://daringfireball.net/projects/smartypants/
.. _`pseudo-protocols`:
     http://www.pell.portland.or.us/~orc/Code/discount/#pseudo


Using ``libmarkdown``
---------------------

If you are familiar with using the C library and would rather use
Discount library directly, ``libmarkdown`` is what you are looking
for; it's simply a thin wrapper around the original C implementation.
``libmarkdown`` exposes the public functions and flags documented on
the `Discount homepage`_.

In Python you'll need to do some extra work preparing Python objects
you want to pass to ``libmarkdown``'s functions.

Most of these functions accept ``FILE*`` and ``char**`` types as their
arguments, which require some additional ctypes boilerplate.

To get a ``FILE*`` from a Python file descriptor for use with
``libmarkdown``, use the following pattern::

    i = ctypes.pythonapi.PyFile_AsFile(sys.stdin)
    o = ctypes.pythonapi.PyFile_AsFile(sys.stdout)
    doc = libmarkdown.mkd_in(i, 0)
    libmarkdown.markdown(doc, o, 0))

For ``libmarkdown`` functions to which you pass a ``char**``, use the
following pattern::

    cp = ctypes.c_char_p('')
    ln = libmarkdown.mkd_document(doc, ctypes.byref(cp))
    html_text = cp.value[:ln]

It is important to initialize ``c_char_p`` with an empty string.

.. _`Discount homepage`:
   http://www.pell.portland.or.us/~orc/Code/discount/


Running the test suite
----------------------

Tests are available with the source distibution of ``discount`` in the
``tests.py`` file.  The C shared object should be compiled first::

    python setup.py build_ext

Then you can run the tests::

    python tests.py


Source code and reporting bugs
------------------------------

You can obtain the source code and report bugs on
`GitHub project page`_.

.. _`GitHub project page`:
   http://github.com/trapeze/python-discount/issues


License
-------

See the ``LICENSE`` file in the source distribution for details.


Credits
-------

The `Discount`_ C library is written and maintained by `David Parson`_
and contributors.  See the ``AUTHORS`` file for details.  The python
``discount`` binding is maintained by `Tamas Kemenczy`_, and is funded
by `Trapeze`_.

.. _`Discount`:    http://www.pell.portland.or.us/~orc/Code/discount/
.. _`David Parson`: http://www.pell.portland.or.us/~orc
.. _`Tamas Kemenczy`: mailto:tkemenczy@trapeze.com
.. _`Trapeze`: http://trapeze.com
