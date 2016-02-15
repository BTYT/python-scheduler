#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Appbuilder
"""

from lib.configure import get_configs
from lib.DB import MySQL
import os
import sys
import datetime
import time
import hashlib
import json
import re

FILE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class Appbuilder(object): 

    """Appbuilder
    """

    def __init__(self, confPath=None):
        """__init__
        """

        if not confPath:
            confPath = os.path.join(FILE_PATH, "conf", "db.conf")
        data = get_configs(confPath)
        self.db_handle = MySQL(data['appbuilder'])

    def test2(self, **kwargs): 
        """test2
        """

        print time.time()
        print "test2 from appbuilder"
        print kwargs

