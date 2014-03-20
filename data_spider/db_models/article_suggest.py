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

class ArticleSuggest(object):

    _conn = settings.mongoConn
    coll = _conn['data_center']['article_suggest']

    @classmethod
    @mongo_exception
    def is_exist(cls,id):
        isv = cls.coll.find_one({'_id':id})
        if isv is None:
            return False
        else:
            return True

    @classmethod
    @mongo_exception
    def upset_artice_suggest(cls,obj_dict):
        filter = {'_id':obj_dict["id"]}
        if obj_dict.has_key('_id'):
            del shop_dict['_id']
        cls.coll.update(filter, {'$set':obj_dict}, upsert=False)

    @classmethod
    @mongo_exception
    def insert_article_suggest(cls,obj_dict):
        obj_dict["_id"] = obj_dict["id"]
        cls.coll.save(obj_dict)

    @classmethod
    @mongo_exception
    def upsert_article_suggest_list(cls,data_list):
        for data in data_list:
            if cls.is_exist(data["id"]): 
                cls.upset_artice_suggest(data)
            else:
                cls.insert_article_suggest(data)

