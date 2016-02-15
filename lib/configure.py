#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""
获取配置信息公用模块

Authors: zhouwenhong(zhouwenhong@baidu.com)
Date:    2015/01/14
"""
import os
import ConfigParser


def get_configs(filePath):
    """获取配置文件所有配置信息

    Args:
        filePath: 配置文件路径

    Returns:
        A dict. For example:
        {
            'db': {
                'db_user': 'xxxx', 
                'db_port': '3306', 
                'db_pass': 'xxxxxx', 
                'db_name': 'xxxx', 
                'db_host': '10.10.10.10', 
                'db_charset': 'utf8'
            }
        }

    Raises:
        IOError: 配置文件路径不存在
    """
    if not os.path.isfile(filePath):
        raise IOError("config file is not exist.")

    data = {}
    conf = ConfigParser.ConfigParser()
    conf.read(filePath)

    for section in conf.sections():
        data[section] = {}
        for attr in conf.options(section):
            data[section][attr] = conf.get(section, attr)

    return data
