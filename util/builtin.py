# -*- encoding: utf-8 -*-
'''
Built-in functions of Python interpreter.

For there are several functions that appear under different namespaces 
in Python2 and Python3, so I wrote this utility to provide a general interface 
to use these builtin functions. 

@author: pwx
@date: 2012-2-9
'''
from __future__ import unicode_literals, print_function, nested_scopes, division
import sys

# Please list all the modules you imported here for automatically reload.
_DEPENDENCY_ = []

# import module
if (sys.version_info.major == 2):
    from avalon.util.py2x import builtin_2x
    _DEPENDENCY_.append(builtin_2x)
else:
    from avalon.util.py3x import builtin_3x
    _DEPENDENCY_.append(builtin_3x)

####
# expose builtin functions
#
__m = _DEPENDENCY_[0]

# interpreter
reload = __m.reload
callable = __m.callable

iterkeys = __m.iterkeys
iteritems = __m.iteritems
itervalues = __m.itervalues

keys = __m.keys
items = __m.items
values = __m.values

