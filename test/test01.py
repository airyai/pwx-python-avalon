# -*- encoding: utf-8 -*-
'''
Test log device.

@author: pwx
@date: 2012-2-10
'''
from __future__ import unicode_literals, print_function, nested_scopes, division

# Please list all the modules you imported here for automatically reload.
from avalon.util import builtin, object, baselog
_DEPENDENCY_ = [builtin, object, baselog]

# do test
print (baselog._loggers['console'])

baselog.fatal('Shutdown.')
baselog.error('Oh, no!')
baselog.warning('Hello, world!')
baselog.info('Are you ok?')
baselog.debug('Bug or not.')
baselog.log('Hey!', 12)

baselog.setLevel(baselog.ERROR)
baselog.warning('You cannot see me!')

baselog.setLevel(baselog.NOTSET)
baselog.warning('You can now see me!')

try:
    0/0
except:
    baselog.exception('Exception logged.')

