from __future__ import unicode_literals

from parser import (matchiter, matchall, selrule_or_atom_re,
    selrule_or_any_re, sel_re, atom_re)
import logging


logger = logging.getLogger(__name__)


def isolcss(prefix, css):
    """
    Returns `css` with all selectors prefixed by `prefix`, or replacing "&"
    as SASS and LESS both do.

    Tries to parse strictly then falls back, with a warning, to forgiving
    parse if necessary.
    """
    try:
        # Attempt full strict parse, raise exception on failure.
        all(True for m in matchiter(selrule_or_atom_re, css))
    except ValueError as e:
        logger.warning("Strict parse failed at char {}".format(e.args[0]))
        splits = matchiter(selrule_or_any_re, css)
    else:
        splits = matchiter(selrule_or_atom_re, css)

    css = []

    for m in splits:
        if not m.groupdict()['sels']:
            css.extend(m.group(0))
            continue

        sels = matchall(sel_re, m.group('sels'))

        # This should never happen because sel_re is a subpattern
        # of the original match.
        assert sels, "Failed to split selectors: {!r}".format(m.group('sels'))

        for sel in sels:
            atoms = matchall(atom_re, sel)
            if '&' in atoms:
                sel = ''.join((prefix if a == '&' else a) for a in atoms)
            else:
                sel = '%s %s' % (prefix, sel)
            css.append(sel)
        css.append(m.group('ruleset'))

    return ''.join(css)
