# -*- encoding: utf-8 -*-
'''
A general interface for all objects in avalon project.

@author: pwx
@date: 2012-2-5
'''
from __future__ import unicode_literals, print_function, nested_scopes, division
import sys

# Please list all the modules you imported here for automatically reload.
_DEPENDENCY_ = []
__ALL__ = ['Object']

# Expose a suitable object class.
if sys.version_info.major == 2:
    from avalon.util.py2x import object_2x
    from avalon.util.py2x.object_2x import Object
    _DEPENDENCY_.append(object_2x)
else:
    from avalon.util.py3x import object_3x
    from avalon.util.py3x.object_3x import Object
    _DEPENDENCY_.append(object_3x)
    
#Object = _DEPENDENCY_[0].Object

