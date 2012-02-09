# -*- encoding: utf-8 -*-
'''

@author: pwx
@date: 2012-2-5
'''
from __future__ import unicode_literals, print_function, nested_scopes, division
import avalon.test.material01a
from avalon.test import material01a as m2

# Please list all the modules you imported here for automatically reload.
_DEPENDENCY_ = [avalon.test.material01a, m2]
f = lambda: avalon.test.material01a.value
f2 = lambda: m2.value
value_cache = m2.value
