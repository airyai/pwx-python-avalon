# -*- encoding: utf-8 -*-
'''

@author: pwx
@date: 2012-2-9
'''
from __future__ import unicode_literals, print_function, nested_scopes, division
import __builtin__

# Please list all the modules you imported here for automatically reload.
_DEPENDENCY_ = []

# expose shadowed builtin objects
object = __builtin__.object

# expose reload function
reload = __builtin__.reload

# expose testers
callable = __builtin__.callable

# expose itertools
iteritems = lambda x: x.iteritems()
iterkeys = lambda x: x.iterkeys()
itervalues = lambda x: x.itervalues()

items = lambda x: x.items()
keys = lambda x: x.keys()
values = lambda x: x.values()

# StringIO
from cStringIO import StringIO
