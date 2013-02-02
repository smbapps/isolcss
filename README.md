isolcss
=======

CSS isolator for embedding standalone HTML/CSS into a containing page.

Written by the [PagePart Team][1] and released under the [BSD License][2].

Overview
========

This module consists of a single function `isolcss()` which accepts a block of CSS and a selector prefix, and returns a new block of CSS in which all the selectors have been modified with the prefix.

For example, you might have some CSS which should only apply to an area of the final page:

```scss
p { font-size: 10px; }
h1, h2 { font-weight: bold; }
```

As written this affects the entire page. Call `isolcss('#box', css)` to convert this to:

```scss
#box p { font-size: 10px; }
#box h1, #box h2 { font-weight: bold; }
```

Additionally isolcss recognizes the LESS/SASS ampersand syntax so the following input:

```scss
&.myclass { padding: 20px; }
body & a { text-decoration: none; }
```

results in:

```scss
#box.myclass { font-size: 10px; }
body #box a { text-decoration: none; }
```

Installing isolcss
==================

Install the latest release from pypi:

    pip install isolcss

Running the tests
=================

To run the tests against the current environment:

    python ./tests.py

[1]: http://pagepart.com/
[2]: http://opensource.org/licenses/BSD-2-Clause
