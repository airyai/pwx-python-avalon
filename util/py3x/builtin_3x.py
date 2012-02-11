# -*- encoding: utf-8 -*-
'''

@author: pwx
@date: 2012-2-9
'''
from __future__ import unicode_literals, print_function, nested_scopes, division
import imp, builtins

# Please list all the modules you imported here for automatically reload.
_DEPENDENCY_ = []

# expose shadowed builtin objects
object = builtins.object

# expose reload
reload = imp.reload

# expose testers
# callable = lambda fp: getattr(fp, '__call__') is not None
callable = builtins.callable

# expose itertools
iteritems = lambda x: x.items()
iterkeys = lambda x: x.keys()
itervalues = lambda x: x.values()

items = lambda x: list(x.items())
keys = lambda x: list(x.keys())
values = lambda x: list(x.values)

# StringIO
from io import StringIO
