#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'


import sys
import os
import logging
import logging.config
from datetime import  datetime


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))

from user_center.conf import settings 
from user_center.common.decorator import mongo_exception

class Orders(object):
    """
    class to operate order_info collections
    """

    _conn = settings.user_conn
    coll = _conn['user_center']['orders']

    @classmethod
    @mongo_exception
    def upsert_order(cls,order_dict):
        filter = {'_id':order_dict['order_id']}
        order_dict.update({'_id':order_dict['order_id']})
        cls.coll.update(filter, order_dict, upsert=True)
    
    @classmethod
    @mongo_exception
    def get_all_orders_list(cls):
        orders = cls.coll.find()
        order_list = [order for order in orders]
        return order_list

    @classmethod
    @mongo_exception
    def get_orders_by_nick(cls, nick):
        orders = cls.coll.find({'nick':nick})
        order_list = [order for order in orders]
        return order_list
    
    
    @classmethod
    @mongo_exception
    def get_orders_by_key(cls, key, value):
        orders = cls.coll.find({key:value})
        order_list = [order for order in orders]
        return order_list
    
    @classmethod
    @mongo_exception
    def get_orders_between_time(cls, start_time, end_time):
        orders = cls.coll.find({'create':{'$gte':start_time, '$lte':end_time}})
        order_list = [order for order in orders]
        return order_list

    @classmethod
    @mongo_exception
    def get_orders_count(cls,start_time,end_time,article_code):
        filter={'create':{'$gte':start_time, '$lte':end_time}}
        if article_code is not None:
            filter["article_code"]=article_code
        return cls.coll.find(filter).count()

    @classmethod
    @mongo_exception
    def get_orders_count_between_time(cls, start_time, end_time):
        return  cls.coll.find({'create':{'$gte':start_time, '$lte':end_time}}).count()
        
    @classmethod
    @mongo_exception
    def get_order_by_order_id(cls,order_id):
        return cls.coll.find_one({"_id":order_id})

    @classmethod
    @mongo_exception
    def get_orders_by_fuzzy(cls,fuzzy_nick,item_code,fuzzy_order_cycle_end):
        filter={"item_code":item_code,"nick":{"$regex":fuzzy_nick},"order_cycle_end":{"$gte":fuzzy_order_cycle_end}}
        cursor=cls.coll.find(filter)
        return [doc for doc in cursor]

    @classmethod
    def get_orders_by_dynamic(cls,filter,fields=None):
        """动态查询,按filter条件查询返回fields 列表中指定的字段,如果未指定返回字段则返回去全部"""
        if fields is None or len(fields) ==0:
            cursor = cls.coll.find(filter)
        else:
            field_dict = {}.fromkeys(fields,1)
            cursor = cls.coll.find(filter,field_dict)
        return [doc for doc in cursor]

    @classmethod
    def get_orders_by_nick_list(cls,nick_list,fields=None):
        if not fields:
            cursor = cls.coll.find({"nick":{"$in":nick_list}})
        else:
            field_dict = {}.fromkeys(fields,1)
            cursor = cls.coll.find({"nick":{"$in":nick_list}},field_dict)
        return [doc for doc in cursor]

