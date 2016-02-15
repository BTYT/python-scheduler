#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""clearGolf457
"""

from lib.configure import get_configs
from lib.DB import MySQL
import os
import sys
import datetime
import time

FILE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class ClearGolf457(object): 

    """clearGolf457
    """

    def __init__(self, confPath=None):
        """__init__
        """

        if not confPath:
            confPath = os.path.join(FILE_PATH, "conf", "db.conf")
        self.data = get_configs(confPath)

    def purge(self, **kwargs): 
        """purge old data
        """
        self.db_handle_query = MySQL(self.data[kwargs["purge_db_query"]])
        print kwargs["purge_sql_query"]
        self.db_handle_query.query(kwargs["purge_sql_query"])
        arrData = self.db_handle_query.fetchAllRows()
        if len(arrData) == 0: 
            return
        strIds = ','.join([str(i[kwargs["purge_primary_key"]]) for i in arrData])
        self.db_handle_delete = MySQL(self.data[kwargs["purge_db_delete"]])
        for i in range(1, 10): 
            strSqlKey = "purge_sql_delete_" + str(i)
            if strSqlKey in kwargs:
                strSql = kwargs[strSqlKey]
                strSql = strSql.replace("^__PRIMARY_KEY_LIST__^", strIds)
                print strSql
                self.db_handle_delete.query(strSql)
                
        if "purge_partition_hash_key" in kwargs: 
            arrHashData = {}
            for row in arrData: 
                intHashKey = int(row[kwargs["purge_partition_hash_key"]])
                arrHashData[intHashKey] = intHashKey

            for intHashKey in arrHashData: 
                intHashOffset = eval(str(intHashKey) + kwargs["purge_partition_hash_method"])
                for i in range(1, 10): 
                    strSqlKey = "purge_sql_delete_hash_" + str(i)
                    if strSqlKey not in kwargs: 
                        continue

                    strSql = kwargs[strSqlKey]
                    strSql = strSql.replace("^__PRIMARY_KEY_LIST__^", strIds)
                    strSql = strSql.replace("^__PARTITION_HASH_KEY__^", str(intHashKey))
                    strSql = strSql.replace("^__PARTITION_HASH_VALUE__^", str(intHashOffset))
                    print strSql
                    self.db_handle_delete.query(strSql)

