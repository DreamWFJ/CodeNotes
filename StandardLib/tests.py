# -*- coding: utf-8 -*-
# ===================================
# ScriptName : tests.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-20 14:20
# ===================================

import logging
import logging.config

# logging.config.fileConfig("logger.conf")


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

if __name__ == '__main__':
    test()
    