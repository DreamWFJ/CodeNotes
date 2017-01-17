# -*- coding: utf-8 -*-
# ===================================
# ScriptName : tests.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-20 14:20
# ===================================

import threading

def test():
    print threading.active_count()
    print threading.Condition()
    print threading.currentThread()

if __name__ == '__main__':
    test()