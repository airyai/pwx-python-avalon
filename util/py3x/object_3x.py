# -*- encoding: utf-8 -*-
'''

@author: pwx
@date: 2012-2-5
'''

# Please list all the modules you imported here for automatically reload.
_DEPENDENCY_ = []

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
        return ''
    
    def toRepr(self):
        '''
        Objects that are intended to give a different information 
        other than default repr information <object CLASSNAME toString> 
        should implement this. Also, toRepr should return unicode.
        '''
        obj_to_str = self.toString()
        if (not obj_to_str):
            return '<%s #%s>' % (self.__class__.__name__, hex(id(self)))
        else:
            return '<%s #%s %s>' % (self.__class__.__name__,
                                   hex(id(self)), obj_to_str)
