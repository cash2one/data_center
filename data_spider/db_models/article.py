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

class Article(object):

    _conn = settings.mongoConn
    coll = _conn['data_center']['article']


    @classmethod
    @mongo_exception
    def is_exist(cls,article_code):
        isv = cls.coll.find_one({'_id':article_code})
        if isv is None:
            return False
        else:
            return True

    @classmethod
    @mongo_exception
    def upset_artice(cls,obj_dict):
        filter = {'_id':unicode(obj_dict['article_code'])}
        if obj_dict.has_key('_id'):
            del shop_dict['_id']
        cls.coll.update(filter, {'$set':obj_dict}, upsert=False)

    @classmethod
    @mongo_exception
    def insert_article(cls,obj_dict):
        filter = {'_id':obj_dict['article_code']}
        obj_dict.update({'_id':obj_dict['article_code']})
        cls.coll.save(obj_dict)

    @classmethod
    @mongo_exception
    def upsert_article_list(cls,data_list):
        for data in data_list:
            if cls.is_exist(data["article_code"]):
                cls.upset_artice(data)
            else:
                cls.insert_article(data)

    @classmethod
    @mongo_exception
    def get_articles_by_cat_id(cls,cat_id):
        cursor = cls.coll.find({'cat_id':cat_id})
        return [obj for obj in cursor] 

    @classmethod
    @mongo_exception
    def get_article_by_id(cls, article_code):
        obj = cls.coll.find_one({'_id':article_code})
        return obj 
    
