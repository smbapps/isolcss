"""
Purpose-built CSS parser for isolcss
"""

from __future__ import absolute_import
from __future__ import unicode_literals


# The regex module has optimizations that make this parser faster:
#   ++ is same as + but forbids backtracking.
#   *+ is same as * but forbids backtracking.
try:
    import regex as re
    re.DEFAULT_VERSION = re.V1
    compile = re.compile
except ImportError:
    import re
    def compile(patt, flags=0):
        patt = patt.replace('++', '+')
        patt = patt.replace('*+', '*')
        return re.compile(patt, flags)

try:
    basestring
except NameError:
    # Hello Python 3
    basestring = str


comment = r'''(?:
    /\*                 # start comment
    (?: [^*]++          # anything except *
      | \*(?!/)         # * unless followed by /
      )*+               # zero or more
    \*/                 # end comment
    )'''

quoted = r'''(?:
    "                   # start double quote
    (?: [^"\\\r\n]++    # anything except \ cr or nl
      | \\(\r\n|.|\s)   # \ followed by crnl or anything
      )*+               # zero or more, no backtracking
    "                   # end double quote
  | '                   # OR start single quote
    (?: [^'\\\r\n]++    # anything except \ cr or nl
      | \\(\r\n|.\s)    # \ followed by crnl or anything
      )*+               # zero or more
    '                   # end single quote
    )'''

atom = r'''(?:
    %(quoted)s          # quoted
  | [^"']               # or any non-quote chars
    )''' % locals()

comment_or_atom = r'''(?:
    %(comment)s         # comment
  | %(quoted)s          # or quoted
  | [^"'/]              # or any non-quote non-comment chars
  | /(?!\*)             # or / unless followed by *
    )''' % locals()

selattr = r'''(?:
    \[                  # start attribute selector
    (?: %(quoted)s      # quoted string
      | [^]]            # or anything except closing bracket
      )*+               # zero or more
    \]                  # end attribute selector
    )''' % locals()

# This pattern includes } as a delimeter to avoid getting tangled in
# @-rules that we don't care about.
sel = r'''(?:
    (?!\s)              # selector starts with non-ws
    (?!%(comment)s)     # selector starts with non-comment
    (?: %(selattr)s     # attribute selector
      | %(quoted)s      # or quoted string
      | [^{}"',]        # or non-delimeters
      )+                # one or more
    )''' % locals()

comma = r'''(?:
    (?:%(comment)s|\s)*+  # comments and/or whitespace
    ,                     # delimiting comma
    (?:%(comment)s|\s)*+  # comments and/or whitespace
    )''' % locals()

selcomma = r'''(?:
    (?P<sel> %(sel)s )      # selector
    (?P<comma> %(comma)s    # separated by delimeter
      | (?:%(comment)s|\s)* # or ended by comments and/or whitespace
        (?!%(sel)s) )       # unless followed by selector
    )''' % locals()

# This pattern includes { as a delimeter so that a ruleset never contains
# nested rules. This forces selectors to match only on inner rules (in the
# case of @-rules).
ruleset = r'''(?:
    \{                  # start ruleset
    (?: %(comment)s     # comment
      | %(quoted)s      # or quoted
      | [^{}"']         # or non-delimeters
      )*+               # zero or more
    \}                  # end ruleset
    )''' % locals()

selrule = r'''(?:
    (?P<sels> %s+ )     # selectors
    (?P<ruleset> %s )   # followed by a ruleset
    )''' % (selcomma, ruleset)


# Compile the three final patterns.
# The first two are for strict and forgiving parsing, respectively.
# The last pattern is for splitting selectors on commas.
atom_re = compile(atom, re.X)
selrule_or_atom_re = compile(r'%s|%s' % (selrule, comment_or_atom), re.X)
selrule_or_any_re = compile(r'%s|.|\s' % selrule, re.X)
sel_re = compile(selcomma, re.X)


def matchiter(r, s, flags=0):
    """
    Yields contiguous MatchObjects of r in s.
    Raises ValueError if r eventually doesn't match contiguously.
    """
    if isinstance(r, basestring):
        r = re.compile(r, flags)
    while s:
        m = r.match(s)
        if not m or not m.group(0):
            raise ValueError(s)
        s = s[len(m.group(0)):]
        yield m


def matchall(r, s, flags=0):
    """
    Returns the list of contiguous string matches of r in s,
    or None if r does not successively match the entire s.
    """
    try:
        return [m.group(0) for m in matchiter(r, s, flags)]
    except ValueError:
        return None
