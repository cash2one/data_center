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

class ArticleBase(object):

    _conn = settings.mongoConn
    coll = _conn['data_center']['article_base']


    @classmethod
    @mongo_exception
    def is_exist(cls,article_code,rpt_date):
        #d = datetime.combine(rpt_date,dt.time())
        obj= cls.coll.find_one({'article_code':article_code,"rpt_date":rpt_date})
        if obj is None:
            return False
        else:
            return True

    @classmethod
    @mongo_exception
    def upset_article_base(cls,obj_dict):
        filter = {'article_code':obj_dict['article_code'],"rpt_date":obj_dict["rpt_date"]}
        if obj_dict.has_key('_id'):
            del shop_dict['_id']
        cls.coll.update(filter, {'$set':obj_dict}, upsert=False)

    @classmethod
    @mongo_exception
    def insert_article_base(cls,obj_dict):
        filter = {'article_code':obj_dict['article_code'],"rpt_date":obj_dict["rpt_date"]}
        cls.coll.save(obj_dict)

    @classmethod
    @mongo_exception
    def upsert_article_base_list(cls,data_list):
        for data in data_list:
            if cls.is_exist(data["article_code"],data["rpt_date"]):
                cls.upset_article_base(data)
            else:
                cls.insert_article_base(data)

    @classmethod
    @mongo_exception
    def get_article_base_by_date(cls, article_code,rpt_date):
        obj = cls.coll.find_one({'article_code':article_code,"rpt_date":rpt_date})
        return obj 
    
