# -*- coding: utf-8 -*-
# ===================================
# ScriptName : tests.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-20 14:20
# ===================================

import threading

def haha():
    print "haha"

def test():
    print "threading.setprofile(func): ",threading.setprofile(haha)
    print "threading.current_thread(): ",threading.active_count()
    print "threading.Condition(): ",threading.Condition()
    print "threading.currentThread(): ",threading.currentThread()
    print "threading.enumerate(): ",threading.enumerate()
    print "threading.Event(): ",threading.Event()
    print "threading.local(): ", threading.local()
    # lock 和 rlock 的区别是：lock中多次acquire会死锁，而rlock不会，但必须的有同样次数的release
    b = threading.Lock()
    print b.acquire()
    print b.release()
    print "--------------------------------------------"
    a = threading.RLock(True)
    print a.acquire()
    print a.release()

    print "threading.Semaphore(): "
    c = threading.Semaphore(1)

    c.acquire()
    print "threading.Thread(): ",threading.Thread()
    print "threading.Timer(): ", threading.Timer(10, haha)
    print "threading.settrace: ",threading.settrace(haha)
    c.release()

if __name__ == '__main__':
    test()