# -*- encoding: utf-8 -*-
'''
Cocurrency, synchronize, and other base utilities for threading.

@author: pwx
@date: 2012-2-10
'''
from __future__ import unicode_literals, print_function, nested_scopes, division
import threading

# Please list all the modules you imported here for automatically reload.
from avalon.util import builtin, object
_DEPENDENCY_ = [builtin, object]

######
# Switches
#
MULTI_THREAD_ON = True
THREAD_LOCK_ON = True

######
# thread lock
#
class RLock(object.Object):
    '''
    Wrap threading.RLock, and THREAD_LOCK_ON the global switch 
    for the Lock to be used or not.
    '''
    def __init__(self):
        self._lock = threading.Lock()
        
    def acquire(self, *args, **kwargs):
        if (THREAD_LOCK_ON):
            self._lock.acquire(*args, **kwargs)

    def release(self, *args, **kwargs):
        if (THREAD_LOCK_ON):
            self._lock.release(*args, **kwargs)

class Lock(object.Object):
    '''
    Wrap threading.Lock, and THREAD_LOCK_ON the global switch 
    for the Lock to be used or not.
    '''
    def __init__(self):
        self._lock = threading.Lock()
        
    def acquire(self, *args, **kwargs):
        if (THREAD_LOCK_ON):
            self._lock.acquire(*args, **kwargs)
            
    def acquire_lock(self, *args, **kwargs):
        if (THREAD_LOCK_ON):
            self._lock.acquire_lock(*args, **kwargs)
            
    def release(self, *args, **kwargs):
        if (THREAD_LOCK_ON):
            self._lock.release(*args, **kwargs)
            
    def release_lock(self, *args, **kwargs):
        if (THREAD_LOCK_ON):
            self._lock.release_lock(*args, **kwargs)
            
    def locked(self, *args, **kwargs):
        if (THREAD_LOCK_ON):
            self._lock.locked(*args, **kwargs)
            
    def locked_lock(self, *args, **kwargs):
        if (THREAD_LOCK_ON):
            self._lock.locked_lock(*args, **kwargs)
