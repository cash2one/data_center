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

class Refunds(object):
    """
    class to operate refund_info collections
    """

    _conn = settings.user_conn
    coll = _conn['user_center']['refunds']

    @classmethod
    @mongo_exception
    def upset_refund(cls,refund_dict):
        filter = {'_id':refund_dict['order_id']}
        if refund_dict.has_key('_id'):
            del refund_dict['_id']
        cls.coll.update(filter, {'$set':refund_dict}, upsert=False, j=True)

    @classmethod
    @mongo_exception
    def upsert_refund(cls,refund_dict):
        filter = {'_id':refund_dict['order_id']}
        refund_dict.update({'_id':refund_dict['order_id']})
        cls.coll.update(filter, refund_dict, upsert=True, j=True)

    @classmethod
    @mongo_exception
    def del_refund(cls,refund_id):
        cls.coll.remove({"_id":refund_id},j=True)
    
    @classmethod
    @mongo_exception
    def get_all_refunds_list(cls):
        refunds = cls.coll.find()
        refund_list = [refund for refund in refunds]
        return refund_list

    @classmethod
    @mongo_exception
    def get_refunds_by_nick(cls, nick):
        refunds = cls.coll.find({'nick':nick})
        refund_list = [refund for refund in refunds]
        return refund_list
    
    @classmethod
    @mongo_exception
    def get_refunds_by_key(cls, key, value):
        refunds = cls.coll.find({key:value})
        refund_list = [refund for refund in refunds]
        return refund_list
    
    @classmethod
    @mongo_exception
    def get_refunds_between_time(cls, start_time, end_time):
        refunds = cls.coll.find({'occur_time':{'$gte':start_time, '$lte':end_time}})
        refund_list = [refund for refund in refunds]
        return refund_list

    @classmethod
    @mongo_exception
    def get_refund_by_refund_id(cls,refund_id):
        refund=cls.coll.find_one({"_id":refund_id})
        return refund

    @classmethod
    @mongo_exception
    def get_refunds_by_ids(cls,refund_id_list):
        refund_list=cls.coll.find({"_id":{"$in":refund_id_list}})
        refund_list=[refund for refund in refund_list]
        return refund_list
