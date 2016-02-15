#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""whitehand
"""

import os
from lib.configure import get_configs
import threading
import time
import datetime
import sys
import logging


from apscheduler.schedulers.blocking import BlockingScheduler


FILE_PATH = (os.path.dirname(os.path.realpath(__file__)))
confPath = os.path.join(FILE_PATH, "conf", "whitehand.conf")
arrScripts= get_configs(confPath)

#{'script_threads': {'period': '10', 'filename': 'b.py'}}


def getObj(_cls_name): 
    """
    python反射
    """
    _packet_name = 'scriptthreads.' + _cls_name
    _module_home = __import__(_packet_name, globals(), locals(), [_cls_name])
    obj =  getattr(_module_home, _cls_name)
    return obj





def main():
    """main
    """
    print arrScripts
    logging.basicConfig()
    objSche = BlockingScheduler()
    for (k, v) in arrScripts.items(): 
        #ThreadNum(v)
        o = getObj(v['classname'])
        f = getattr(o(), v['method'])
        objSche.add_job(f, 'cron', month=v['cron_month'], day=v['cron_day'], 
            hour=v['cron_hour'], minute=v['cron_minute'], kwargs=v)

    objSche.start()


if __name__ == "__main__": 
    main()

