#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Test dependency map.

@author: pwx
@date: 2012-2-9
'''
from __future__ import unicode_literals, print_function, nested_scopes, division
import os

# Please list all the modules you imported here for automatically reload.
import avalon.util.dependency as dep
from avalon.util import builtin, module
_DEPENDENCY_ = [dep, builtin, module]

import unittest


class Test(unittest.TestCase):
    data = [
            [1,2],
            [3],
            [1,3],
            [],
        ]
    
    def fp_dep(self, v):
        return Test.data[v]
    
    def dmap_targets_agree(self, dmap):
        for k,v in builtin.iteritems(dmap.nodes):
            # check targets
            s1 = set(Test.data[k])
            s2 = set(v.targets)
            if (s1 != s2):
                return False
            # check rev
            for x in v.parents:
                if k not in dmap.nodes[x].targets:
                    return False
            # check parent rev
            for x in v.targets:
                if k not in dmap.nodes[x].parents:
                    return False
        return True

    def test_dependency_add_remove(self):
        '''
        Test add & remove features on dependency map.
        '''
        dmap = dep.DependencyMap(self.fp_dep)
        # push data
        Test.data = [
            [1,2],
            [3],
            [1,3],
            [],
        ]
        dmap.push(range(0, len(Test.data)))
        # check state
        self.assertTrue(len(dmap.nodes) == len(Test.data),
                        'Dmap data size does not agree.')
        self.assertTrue(list(dmap.nodes.keys()) == [0,1,2,3],
                        'Dmap data value does not agree.')
        self.assertTrue(self.dmap_targets_agree(dmap),
                        'Dmap node targets does not agree.')
        # update & check state
        Test.data = [
            [1,2,3],
            [3],
            [1,3],
            [1],
        ]
        # dmap.push(range(0, len(Test.data)))
        dmap.refresh()
        self.assertTrue(self.dmap_targets_agree(dmap),
                        'Dmap node targets does not agree after refresh.')
        # remove & check state
        dmap.remove(3)
        Test.data = [
            [1,2],
            [],
            [1],
        ]
        self.assertTrue(self.dmap_targets_agree(dmap),
                        'Dmap node targets does not agree after remove.')
        
    def test_reload_module(self):
        '''
        Test module dependency managed reload.
        
        Codes samples are the same as unittest01.
        '''
        from avalon.test import material01a
        from avalon.test import material01b
        builtin.reload(material01a)
        self.assertTrue (material01a.value != material01b.value_cache,
                         'Material01b will not be automatically reloaded when '
                         'material01a is reloading.')
        v = material01a.value
        module.reload_dir(os.path.dirname(material01b.__file__), [material01b])
        self.assertTrue (v != material01a.value,
                         'Material01a should be managed reloaded while material01b '
                         'is reloading.')
        self.assertTrue (material01a.value == material01b.value_cache,
                         'Material01a should be reloaded before material01b, '
                         'thus material01b.value_cache should just be material01a.value.')
        
    def test_dependency_walk(self):
        '''Test dependency walk.'''
        dmap = dep.DependencyMap(self.fp_dep)
        # push data
        Test.data = [
            [1,2],
            [3],
            [1,3],
            [],
        ]
        dmap.push(range(0, len(Test.data)))
        # dump data
        arr = []
        fp_dump = lambda x: arr.append(x)
        ret_dump = [3, 1, 2, 0]
        dmap.walk(fp_dump)
        self.assertTrue(ret_dump == arr,
                        'Dmap walk result does not agree: expect %s, '
                        'but got %s.' % (ret_dump, arr))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    