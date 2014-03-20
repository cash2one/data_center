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

class SyncStatus(object):

    _conn = settings.mongoConn
    coll = _conn['data_center']['sync_status']


    @classmethod
    @mongo_exception
    def is_exist(cls,article_code):
        isv = cls.coll.find_one({'_id':unicode(article_code)})
        if isv is None:
            return False
        else:
            return True

    @classmethod
    @mongo_exception
    def upset_sync_status(cls,obj_dict):
        filter = {'_id':unicode(obj_dict['article_code'])}
        if obj_dict.has_key('_id'):
            del shop_dict['_id']
        cls.coll.update(filter, {'$set':obj_dict}, upsert=False)

    @classmethod
    @mongo_exception
    def insert_sync_status(cls,obj_dict):
        filter = {'_id':unicode(obj_dict['article_code'])}
        obj_dict.update({'_id':unicode(obj_dict['article_code'])})
        cls.coll.save(obj_dict)

    @classmethod
    @mongo_exception
    def get_sync_status_by_id(cls, article_code):
        obj = cls.coll.find_one({'_id':unicode(article_code)})
        return obj
    
