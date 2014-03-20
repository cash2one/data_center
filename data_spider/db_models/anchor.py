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

class Anchor(object):

    _conn = settings.mongoConn
    coll = _conn['data_center']['anchor']


    @classmethod
    def __get_id(cls,uid,type):
        return hash(str(uid)+str(type))

    @classmethod
    @mongo_exception
    def is_exist(cls,uid,type):
        isv = cls.coll.find_one({'_id':cls.__get_id(uid,type)})
        if isv is None:
            return False
        else:
            return True

    @classmethod
    @mongo_exception
    def upset_anchor(cls,obj_dict):
        id = cls.__get_id(obj_dict["uid"],obj_dict["type"])
        filter = {'_id':id}
        if obj_dict.has_key('_id'):
            del shop_dict['_id']
        cls.coll.update(filter, {'$set':obj_dict}, upsert=False)

    @classmethod
    @mongo_exception
    def insert_anchor(cls,obj_dict):
        id = cls.__get_id(obj_dict["uid"],obj_dict["type"])
        obj_dict.update({'_id':id})
        cls.coll.save(obj_dict)

    @classmethod
    @mongo_exception
    def upsert_anchor_list(cls,data_list):
        for data in data_list:
            if cls.is_exist(data["uid"],data["type"]):
                cls.upset_anchor(data)
            else:
                cls.insert_anchor(data)

