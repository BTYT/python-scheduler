#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""MySQLdb常用函数封装类

依赖库：python-mysql
Authors: zhouwenhong(zhouwenhong@baidu.com)
Date:    2015/01/14
"""

import MySQLdb
import time
import traceback

class MySQL(object):

    """MySQLdb常用函数封装类

    Attributes:
        dbconfig: A dict contains db config.
    Usage:
        db_handle = MySQL(dbconfig)
        db_handle.query("select * from your_table")
        result = db_handle.fetchAllRows();
        db_handle.close()
    """

    def __init__(self, dbconfig):
        """创建MySQL连接
        """
        try:
            self.db_handle = MySQLdb.connect(host=dbconfig["db_host"],
                                         port=int(dbconfig["db_port"]),
                                         user=dbconfig["db_user"],
                                         passwd=dbconfig["db_pass"],)

            self.db_charset = dbconfig["db_charset"]
            
            self.db_handle.autocommit(False) #禁止自动提交
            self.db_handle.set_character_set(self.db_charset)
            self.db_handle.select_db(dbconfig["db_name"])

        except MySQLdb.Error as  error:
            raise Exception(u"数据库错误代码: %s %s" % (error.args[0], error.args[1]))

        self.cursor = self.db_handle.cursor(cursorclass = MySQLdb.cursors.DictCursor)

    def query(self, sql, param=None):
        """执行 SELECT 语句
        """
        try:
            self.cursor.execute("SET NAMES %s" % self.db_charset)
            result = self.cursor.execute(sql, param)
        except MySQLdb.Error as  e:
            print "数据库错误代码:", e.args[0], e.args[1]
            result = False
        return result

    def update(self, sql, param=None):
        """执行 UPDATE 及 DELETE 语句
        """
        try:
            self.cursor.execute("SET NAMES %s" % self.db_charset)
            result = self.cursor.execute(sql, param)
        except MySQLdb.Error as  e:
            print "数据库错误代码:", e.args[0], e.args[1]
            result = False
        return result

    def executeBatch(self, sql, param=None):
        """批量执行

        # 执行单条sql语句,但是重复执行参数列表里的参数,返回值为受影响的行数
        sql=”insert into cdinfo values(0,%s,%s,%s,%s,%s)”
        #每个值的集合为一个tuple,整个参数集组成一个tuple,或者list
        param=((title,singer,imgurl,url,alpha),(title2,singer2,imgurl2,url2,alpha2))
        #使用executemany方法来批量的插入数据.这真是一个很酷的方法!
        result=cursor.executemany(sql,param)
        """
        try:
            self.cursor.execute("SET NAMES %s" % self.db_charset)
            result = self.cursor.executemany(sql, param)
        except:
            result = 0

        return result

    def insert(self, sql, param=None):
        """执行 INSERT 语句。如主键为自增长int，则返回新生成的ID
        """
        try:
            self.cursor.execute("SET NAMES %s" % self.db_charset)
            self.cursor.execute(sql, param)
            return self.db_handle.insert_id()
        except MySQLdb.Error as  e:
            print "数据库错误代码:", e.args[0], e.args[1]
            return False

    def fetchAllRows(self):
        """返回结果列表
        """
        return self.cursor.fetchall()

    def fetchOneRow(self):
        """返回一行结果，然后游标指向下一行。到达最后一行以后，返回None
        """
        return self.cursor.fetchone()

    def getRowCount(self):
        """获取结果行数
        """
        return self.cursor.rowcount

    def commit(self):
        """数据库commit操作
        """
        self.db_handle.commit()

    def rollback(self):
        """数据库回滚操作
        """
        self.db_handle.rollback()

    def __del__(self):
        """释放资源
        """
        try:
            self.cursor.close()
            self.db_handle.close()
        except:
            pass

    def close(self):
        """关闭数据库连接
        """
        self.__del__()
