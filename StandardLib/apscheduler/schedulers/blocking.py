# -*- coding: utf-8 -*-
from __future__ import absolute_import

from threading import Event

from apscheduler.schedulers.base import BaseScheduler, STATE_STOPPED
from apscheduler.util import TIMEOUT_MAX


class BlockingScheduler(BaseScheduler):
    """
    A scheduler that runs in the foreground
    (:meth:`~apscheduler.schedulers.base.BaseScheduler.start` will block).
    """
    _event = None

    def start(self, *args, **kwargs):
        # 时间初始化默认阻塞，只有调用set才会解除阻塞，clear是重新阻塞
        self._event = Event()
        super(BlockingScheduler, self).start(*args, **kwargs)
        self._main_loop()

    def shutdown(self, wait=True):
        super(BlockingScheduler, self).shutdown(wait)
        self._event.set()

    def _main_loop(self):
        wait_seconds = TIMEOUT_MAX
        while self.state != STATE_STOPPED:
            # 等待超时
            self._event.wait(wait_seconds)
            self._event.clear()
            wait_seconds = self._process_jobs()

    def wakeup(self):
        self._event.set()
