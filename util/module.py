# -*- encoding: utf-8 -*-
'''
This module provides several functions to manage runtime modules.

@author: pwx
@date: 2012-2-5
'''
from __future__ import unicode_literals, print_function, nested_scopes, division
import sys, os, types

# Please list all the modules you imported here for automatically reload.
from avalon.util import dependency, builtin
_DEPENDENCY_ = [dependency, builtin]

#  the following fetched from 1.5.2's inspect.py
def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back

if hasattr(sys, '_getframe'): currentframe = lambda: sys._getframe(1)
# done fetch

# the following fetched from python 2.7 logging module
# and edited by airyai@gmail.com

# not support for frozen exe yet.
def get_source_file(filepath):
    if filepath[-4:].lower() in ['.pyc', '.pyo']:
        filepath = filepath[:-4] + '.py'
    filepath = os.path.normcase(filepath)
    return filepath

_srcfile = get_source_file(__file__)

def get_caller(exclude_files=None):
    '''
    Get the caller script file via stack frame.
    
    @param exclude_files: A list of absolute paths for get_caller to exclude.
    '''
    try:
        f = currentframe()
    except ValueError:
        return ''
    #On some versions of IronPython, currentframe() returns None if
    #IronPython isn't run with -X:Frames.
    exclude_files = set(exclude_files) if exclude_files is not None else set()
    exclude_files.add(_srcfile)
    if f is not None:
        f = f.f_back
    rv = None
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename in exclude_files:
            f = f.f_back
            continue
        rv = (co.co_filename, f.f_lineno, co.co_name)
        break
    return rv
# done fetch

def get_module_name(base_package_name=None, absolute_file_path=None):
    '''
    Get the module name of the caller according to base 
    package name.
    
    The method guesses the module according the script 
    file path via stack frame.
    
    @param base_package_name: The base package name.
    @param absolute_file_path: The module file path.
        If file path is None, then get_caller() will 
        be called to get the module's file path.
    '''
    # get stack frame of the caller
    filepath = absolute_file_path
    if filepath is None:
        rv = get_caller()
        if rv is None:
            return None
        filepath = rv[0]
    base_package_name = os.path.normcase(base_package_name)
    # split the path
    parts = filepath.split(os.path.sep)
    if (not parts):
        return ''
    # remove file extension
    test_str = os.path.splitext(parts[-1])
    if (test_str[1].lower() in ['.py', '.pyc', '.pyo']):
        parts[-1] = test_str[0]
    if (parts[-1] == '__init__'): # check if dir package
        parts = parts[0:-1]
    parts = [i for i in parts if i]
    if (base_package_name is None):
        return '.'.join(parts)
    for i in range(0, len(parts)):
        if (parts[i] == base_package_name):
            return '.'.join(parts[i:])
    # if base not found, return the entire path as package name
    return '.'.join(parts)

######
# Module dependency map
#
def reload_if(predictor = lambda x: True, modules = None):
    '''
    Reload python modules if prediction is True.
    
    @param predictor: A function object that tests modules.
    @param modules: Reload these modules. If modules is None, 
        then all modules will be selected.
    '''
    # define functions
    def fp_dep(mod):
        if (not isinstance(mod, types.ModuleType)):
            return None
        h = getattr(mod, '_DEPENDENCY_', None)
        if (h is not None):
            return h
        return None
    def fp_walk(mod):
        if (predictor(mod)):
            #TODO: log
            # print ('reload %s' % mod.__file__)
            builtin.reload(mod)
    # build dependency map
    dmap = dependency.DependencyMap(fp_dep)
    dmap.push(builtin.itervalues(sys.modules))
    # reload modules
    dmap.walk(fp_walk, modules)
    
def reload_dir(dirpath, modules=None):
    '''
    Reload all modules under specified directory.
    
    @param dirpath: Directories that modules in.
    @param modules: Reload these modules. If modules is None, 
        then all modules will be selected.
    '''
    p = os.path.normpath(os.path.normcase(os.path.abspath(dirpath)))
    p = p.split(os.path.sep)
    def fp_test(x):
        p2 = os.path.normcase(x.__file__)
        p2 = p2.split(os.path.sep)
        if (len(p) > len(p2)):
            return False
        for i in range(0, len(p)):
            if (p[i] != p2[i]):
                return False
        return True
    reload_if(fp_test, modules)
    
    