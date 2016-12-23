# -*- coding: utf-8 -*-
# ===================================
# ScriptName : tests.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-20 14:20
# ===================================

import logging
import logging.config
import traceback
# logging.config.fileConfig("logger.conf")
import sys

def test():
    FileName = ""
    FileMode = "w"
    DateFMT = "%a, %d %b %Y %H:%M:%S"
    Level = logging.DEBUG
    Stream = None
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(
        format=FORMAT,
        datefmt=DateFMT,
        level=Level
    )
    d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
    logger = logging.getLogger('tcpserver')
    logger.warning('Protocol problem: %s', 'connection reset', extra=d)
    try:
        raise KeyError('this is a mesage')
    except:
        e = sys.exc_info()
        a = e[0]
        b = e[1]
        c = e[2]
        print e

def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back

if hasattr(sys, '_getframe'): currentframe = lambda: sys._getframe(3)

import os

_srcfile = os.path.normcase(currentframe.__code__.co_filename)
print _srcfile
def findCaller():
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    f = currentframe()
    #On some versions of IronPython, currentframe() returns None if
    #IronPython isn't run with -X:Frames.
    if f is not None:
        f = f.f_back
    rv = "(unknown file)", 0, "(unknown function)"
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == _srcfile:
            f = f.f_back
            continue
        rv = (co.co_filename, f.f_lineno, co.co_name)
        break
    return rv

def test_1():
    raise KeyError

def test_2():
    try:
        test_1()
    except:
        a = sys.exc_info()
        b = a[2]
        if hasattr(b, 'f_back'):
            print b.f_back
        if hasattr(b, 'f_code'):
            print b.f_code
            print b.f_lineno

if __name__ == '__main__':
    # test()
    test_2()