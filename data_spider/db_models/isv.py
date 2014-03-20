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

class Isv(object):

    _conn = settings.mongoConn
    coll = _conn['data_center']['isv']


    @classmethod
    @mongo_exception
    def is_exist(cls,isv_id):
        isv = cls.coll.find_one({'_id':unicode(isv_id)})
        if isv is None:
            return False
        else:
            return True

    @classmethod
    @mongo_exception
    def upset_isv(cls,obj_dict):
        filter = {'_id':unicode(obj_dict['isv_id'])}
        if obj_dict.has_key('_id'):
            del shop_dict['_id']
        cls.coll.update(filter, {'$set':obj_dict}, upsert=False)

    @classmethod
    @mongo_exception
    def insert_isv(cls,obj_dict):
        filter = {'_id':unicode(obj_dict['isv_id'])}
        obj_dict.update({'_id':unicode(obj_dict['isv_id'])})
        cls.coll.save(obj_dict)

    @classmethod
    @mongo_exception
    def upsert_isv_list(cls,isv_list):
        for isv in isv_list:
            if cls.is_exist(isv["isv_id"]):
                cls.upset_isv(isv)
            else:
                cls.insert_isv(isv)


    @classmethod
    @mongo_exception
    def get_isv_by_id(cls, isv_id):
        isv = cls.coll.find_one({'_id':unicode(isv_id)})
        return isv
    
