#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""
网络爬虫模块

Authors: zhouwenhong(zhouwenhong@baidu.com)
Date:    2015/01/14
Usage:
    spider = UrlSpiders('http://www.baidu.com', 'get')
    con = spider.getResponse()

"""

import urllib
import urllib2
import traceback

# 设置请求超时时间 10s
TIMEOUT_SECOND = 10

class UrlSpiders(object):
    """数据抓取推送类
    """
    def __init__(self, url, method, params=None):
        self.url = url
        self.method = method.upper()
        self.params = params

    def getResponse(self):
        """响应内容
        """
        if self.method == "GET":
            data = self.getRequest()
        elif self.method == "POST":
            data = self.postRequest()
        else:
            raise ValueError("错误的请求方式，仅支持GET、POST")

        return data

    def getRequest(self):
        """GET请求
        """
        if self.params:
            if self.url.find('?') == -1:
                self.url = self.url + "?" + urllib.urlencode(self.params)
            else:
                self.url = self.url + "&" + urllib.urlencode(self.params)

        req = urllib2.Request(self.url)

        try:
            response = urllib2.urlopen(req, timeout=TIMEOUT_SECOND)
            data = {"code":0, "data": response.read()}
        except:
            data = {"code":1, "data": traceback.format_exc()}

        return data

    def postRequest(self):
        """POST请求
        """
        postData = ""
        if self.params:
            postData = urllib.urlencode(self.params)
        req = urllib2.Request(self.url, postData)
        req.add_header('Content-Type', "application/x-www-form-urlencoded")
        try:
            response = urllib2.urlopen(req, timeout=TIMEOUT_SECOND)
            data = {"code":0, "data": response.read()}
        except:
            data = {"code":1, "data": traceback.format_exc()}

        return data
