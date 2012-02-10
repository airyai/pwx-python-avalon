# -*- encoding: utf-8 -*-
'''

@author: pwx
@date: 2012-2-5
'''

# Please list all the modules you imported here for automatically reload.
from avalon.util import builtin
_DEPENDENCY_ = [builtin]

class Object(object):
    '''
    The base class for all avalon classes.
    '''
    def __init__(self):
        '''
        The constructor of an object.
        '''
        pass
    
    def __str__(self):
        return self.toString()
    
    def __repr__(self):
        return self.toRepr()
    
    def toString(self):
        '''
        All avalon objects should implement toString method 
        to provide a general convertion from objects to strings.  
        Method should return a unicode string however version 
        the python interpreter is. If a different repr information 
        is designed to given, toRepr method should be implemented 
        instead of toString.
        '''
        return self.toRepr()
    
    def toRepr(self, extra=None):
        '''
        Objects that are intended to give a different information 
        other than default repr information <object CLASSNAME extra> 
        should implement this. Also, toRepr should return unicode.
        '''
        if (extra is not None):
            extra_info = ' '.join(['{0}={1}'.format(k, v)
                                    for k, v in builtin.iteritems(extra)])
            return '<{0} #{1} {2}>'.format(self.__class__.__name__, hex(id(self)), extra_info)
        else:
            return '<{0} #{1}>'.format(self.__class__.__name__, hex(id(self)))
