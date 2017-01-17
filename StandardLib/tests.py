# -*- coding: utf-8 -*-
# ===================================
# ScriptName : tests.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-20 14:20
# ===================================

import threading

def test():
<<<<<<< HEAD
    print threading.active_count()
    print threading.Condition()
    print threading.currentThread()
=======
    a = threading.RLock(True)
    a.acquire()
    a.release()
>>>>>>> 7ab09ac0bbdb32def880548e8fbd940d61ab6c49

if __name__ == '__main__':
    test()