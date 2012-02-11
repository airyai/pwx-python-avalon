# -*- encoding: utf-8 -*-
'''
Base logging module for avalon project.

@author: pwx
@date: 2012-2-10
'''
from __future__ import unicode_literals, print_function, nested_scopes, division
import time, traceback, sys, os, threading

# Please list all the modules you imported here for automatically reload.
from avalon.util import builtin, object, module
from avalon.base import basethread
_DEPENDENCY_ = [builtin, object, module, basethread]

# internal variables
_srcfile = module.get_source_file(__file__)

######
# Logging switches
#
LOG_THREAD = True
LOG_PROCESS = True

######
# Logging levels
#
(NOTSET, DEBUG, INFO, WARNING, ERROR, FATAL) = (0, 10, 20, 30, 40, 50)
LEVELS = set((NOTSET, DEBUG, INFO, WARNING, ERROR, FATAL))
LEVEL_NAMES = {NOTSET: 'NOTSET', DEBUG: 'DEBUG', INFO: 'INFO',
               WARNING: 'WARNING', ERROR: 'ERROR', FATAL: 'FATAL'}
def getLevelName(level):
    return LEVEL_NAMES.get(level, None)

def addLevel(level, name):
    '''
    Add named logging level.
    
    @param level: Logging level, must be an integer.
    @param name: Level name, must be a unicode string.
    '''
    LEVELS.add(level)
    LEVEL_NAMES[level] = name
    
def removeLevel(level, name):
    '''
    Remove named logging level.
    
    @param level: Logging level, must be an integer.
    @param name: Level name, must be a unicode string.
    '''
    LEVEL_NAMES.pop(level, None)
    LEVELS.discard(level)

#######
# Logging formats
#

#
#FORMAT = '[{level} {asctime} {shortModule}:{lineno}] {message}'
#TIMEFMT = '%Y/%m/%d %H:%M:%S'
FORMAT = '[{shortLevel} {asctime} {shortModule}:{lineno}] {message}'
TIMEFMT = '%y%m%d %H:%M:%S'

#######
# Base Log
#
class LogMessage(object.Object):
    '''
    Collect interpreter information and make a log message.
    
    Available message variables:
    
    message - Log message body.
    levelno - Log level number.
    level - Log level name.
    shortLevel - Log level short name. If level name is defined, 
        then the first level will be used; otherwise L{no} will be used.
    filename - Source file name. If not support, filename will be None.
    lineno - Source line number.
    funcName - Source method name.
    module - Source module, path relative to avalon.
    shortModule - Source module, name only.
    created - Seconds from 1970/1/1.
    asctime - Time formated by strftime(timefmt).
    thread - Thread ID, or None if not support.
    threadName - ThreadName, or None if not support.
    process - Process ID, or None if not support.
    processName - Python multiprocessing module managed Process Name, or None 
        if not support.
    '''
    PROP_BLACKLIST = set (('toString', 'toRepr', 'makeDict', 'formatException'))
    
    def __init__(self, message, level, extra=None, sformat=None, timefmt=None):
        '''
        Create a log message.
        
        @param message: Log message body.
        @param level: Log level.
        @param extra: Extra variables.
        @param sformat: Message format.
        @param timefmt: Time format.
        '''
        # store input details
        self.message = message
        self.levelno = level
        self.extra = extra if extra is not None else {}
        # formats
        self.format = sformat if sformat is not None else FORMAT
        self.timefmt = timefmt if timefmt is not None else TIMEFMT
        # level information
        self.level = LEVEL_NAMES.get(level, 'Level{0}'.format(level))
        self.shortLevel = LEVEL_NAMES.get(level, '')[:1]
        if (self.shortLevel == ''):
            self.shortLevel = 'L{0}'.format(level)
        # traceback
        self.exc_info = sys.exc_info()
        (self.filename, self.lineno, self.funcName)  = module.get_caller([_srcfile])
        if (self.filename is not None):
            self.module = module.get_module_name('avalon', self.filename)
            self.shortModule = self.module.split('.')[-1]
        else:
            self.module = None
            self.shortModule = None
        # time information
        self.time = time.localtime()
        self.created = time.mktime(self.time)
        self.asctime = time.strftime(self.timefmt, self.time)
        # process information
        self.thread = None
        self.threadName = None
        if (LOG_THREAD):
            try:
                self.thread = threading.current_thread().get_ident()
                self.threadName = threading.current_thread().getName()
            except AttributeError:
                pass
        if not LOG_PROCESS:
            self.processName = None
        else:
            self.processName = 'MainProcess'
            mp = sys.modules.get('multiprocessing')
            if mp is not None:
                # Errors may occur if multiprocessing has not finished loading
                # yet - e.g. if a custom import hook causes third-party code
                # to run when multiprocessing calls import. See issue 8200
                # for an example
                try:
                    self.processName = mp.current_process().name
                except StandardError:
                    pass
        if LOG_PROCESS and hasattr(os, 'getpid'):
            self.process = os.getpid()
        else:
            self.process = None
            
    def makeDict(self):
        '''Make log message format dictionary.'''
        props = dir(self)
        ret = {}
        for p in props:
            if (not p.startswith('_') and p not in LogMessage.PROP_BLACKLIST):
                ret[p] = getattr(self, p)
        ret.update(self.extra)
        return ret
    
    def toString(self):
        return self.format.format(**self.makeDict())
    
    def toRepr(self):
        return object.Object.toRepr(self, self.makeDict())
    
    def formatException(self):
        ''''Format and return the specified exception information as a string.'''
        sio = builtin.StringIO()
        ei = self.exc_info
        traceback.print_exception(ei[0], ei[1], ei[2], None, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == "\n":
            s = s[:-1]
        return s

class BaseLog(object.Object):
    '''
    Base logging object.
    
    @ivar levels: Available logging levels.
    @ivar names: Available logging names.
    @ivar enabled: Switch logging on or off.
    @ivar level: Current set logging level.
    '''
    def __init__(self):
        object.Object.__init__(self)
        # logging switches
        self.enabled = True
        self.level = 0
        # logging formats
        self.format = FORMAT
        self.timefmt = TIMEFMT
        # thread lock
        self._lock = basethread.Lock()
        
    def toRepr(self):
        return object.Object.toRepr(self, {'level': self.level, 'enabled': self.enabled})
        
    def setLevel(self, level):
        self._lock.acquire()
        self.level = level
        self._lock.release()
        
    def writeline(self, data):
        '''Write a line into output buffer.'''
        self._lock.acquire()
        print (data)
        self._lock.release()
        
    def flush(self):
        '''Flush all buffer into device.'''
        pass
    
    def close(self):
        '''Close device and shutdown log.'''
        self.enabled = False
        
    def logException(self, message, level, extra=None):
        '''Print message and dump traceback information on the output buffer.'''
        if (level < self.level or not self.enabled):
            return
        if (not isinstance(message, LogMessage)):
            message = LogMessage(message, level, extra=extra, sformat=self.format, timefmt=self.timefmt)
        self.writeline(message.toString())
        if (message.exc_info[0] is not None):
            self.writeline(message.formatException())
        
    def log(self, message, level, extra=None):
        '''Log the message at specified level.'''
        if (level < self.level or not self.enabled):
            return
        if (not isinstance(message, LogMessage)):
            message = LogMessage(message, level, extra=extra, sformat=self.format, timefmt=self.timefmt)
        self.writeline(message.toString())
    
    # Quick log methods
    def debug(self, message, extra=None):
        self.log(message, DEBUG, extra)
        
    def info(self, message, extra=None):
        self.log(message, INFO, extra)
        
    def warning(self, message, extra=None):
        self.log(message, WARNING, extra)
        
    def error(self, message, extra=None):
        self.log(message, ERROR, extra)
        
    def exception(self, message, extra=None):
        self.logException(message, ERROR, extra)
        
    def fatal(self, message, extra=None):
        self.log(message, FATAL, extra)
    critical = fatal

######
# Global Log Handlers
#
_loggers = { 'console':BaseLog() }

def log(message, level, extra=None):
    '''
    Print a message into all log devices.
    
    @param message: Log message.
    @param level: Log level.
    @param extra: Extra variables.
    '''
    for v in builtin.itervalues(_loggers):
        v.log(message, level, extra)
        
def logException(message, level, extra=None):
    '''
    Print a message and dump traceback into all log devices.
    '''
    for v in builtin.itervalues(_loggers):
        v.logException(message, level, extra)
        
def debug(message, extra=None):
    for v in builtin.itervalues(_loggers):
        v.debug(message, extra)
        
def info(message, extra=None):
    for v in builtin.itervalues(_loggers):
        v.info(message, extra)
        
def warning(message, extra=None):
    for v in builtin.itervalues(_loggers):
        v.warning(message, extra)
        
def error(message, extra=None):
    for v in builtin.itervalues(_loggers):
        v.error(message, extra)
        
def exception(message, extra=None):
    for v in builtin.itervalues(_loggers):
        v.exception(message, extra)
        
def fatal(message, extra=None):
    for v in builtin.itervalues(_loggers):
        v.fatal(message, extra)
critical = fatal

def setLevel(level):
    '''Set the level of all log devices.'''
    for v in builtin.itervalues(_loggers):
        v.setLevel(level)


