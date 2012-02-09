#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Test module reload feature.

@author: pwx
@date: 2012-2-5
'''
from __future__ import unicode_literals, print_function, nested_scopes, division

# Please list all the modules you imported here for automatically reload.
from avalon.util import builtin
_DEPENDENCY_ = [builtin]

import unittest


class Test(unittest.TestCase):


    def test_module_reference_valid_after_reload(self):
        from avalon.test import material01a
        from avalon.test import material01b
        v = material01b.f()
        builtin.reload(material01a)
        self.assertTrue (v != material01a.value,
                         'Material01a is designed to provide a different value each time it is reloaded, '
                         'which is not satisfied.')
        self.assertTrue ((material01a.value == material01b.f()) 
                         and (material01b._DEPENDENCY_[0] == material01a)
                         and (id(material01b._DEPENDENCY_[0]) == id(material01a)),
                         'If there are two modules that one uses another, the master cannot correctly get '
                         'control of the slave module after it is reloaded, which feature is required by '
                         'Avalon framework.')
        self.assertTrue ((material01b._DEPENDENCY_[0] == material01b._DEPENDENCY_[1])
                         and (material01b.f() == material01b.f2()),
                         'Though the object id of reloaded module is same as the original one, you cannot '
                         'use `import Module as Alias` Or `from Module import Module`, which is required by '
                         'Avalon framework.')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    