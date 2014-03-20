#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-03-17 13:18
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import sys
import os
import logging
import logging.config
import datetime as dt
from datetime import  datetime
from data_spider.conf import settings 
from data_spider.common.decorator import  mongo_exception

class ArticleOrder(object):

    _conn = settings.mongoConn
    coll = _conn['data_center']['article_order']


    @classmethod
    def __get_id(cls,nick,pay_time):
        return hash(nick+pay_time.strftime("%Y-%m-%d %H:%M:%S"))

    @classmethod
    @mongo_exception
    def is_exist(cls,nick,pay_time):
        isv = cls.coll.find_one({'_id':cls.__get_id(nick,pay_time)})
        if isv is None:
            return False
        else:
            return True

    @classmethod
    @mongo_exception
    def upset_artice_order(cls,obj_dict):
        id = cls.__get_id(obj_dict["nick"],obj_dict["payTime"])
        filter = {'_id':id}
        if obj_dict.has_key('_id'):
            del shop_dict['_id']
        cls.coll.update(filter, {'$set':obj_dict}, upsert=False)

    @classmethod
    @mongo_exception
    def insert_article_order(cls,obj_dict):
        id = cls.__get_id(obj_dict["nick"],obj_dict["payTime"])
        obj_dict.update({'_id':id})
        cls.coll.save(obj_dict)

    @classmethod
    @mongo_exception
    def upsert_article_order_list(cls,data_list):
        for data in data_list:
            if cls.is_exist(data["nick"],data["payTime"]):
                cls.upset_artice_order(data)
            else:
                cls.insert_article_order(data)

