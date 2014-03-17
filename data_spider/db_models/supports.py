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

class Supports(object):
    """
    class to operate support_info collections
    """

    _conn = settings.user_conn
    coll = _conn['user_center']['supports']

    @classmethod
    @mongo_exception
    def is_exists(cls,support_id):
        """服务支持是否存在"""
        support=cls.coll.find_one({"_id":support_id})
        if support is not None:
            return True
        return False

    @classmethod
    @mongo_exception
    def upset_support(cls,support_dict):
        filter = {'_id':support_dict['support_id']}
        if support_dict.has_key('_id'):
            del support_dict['_id']
        cls.coll.update(filter, {'$set':support_dict}, upsert=False, j=True)

    @classmethod
    @mongo_exception
    def upsert_support(cls,support_dict):
        filter = {'_id':support_dict['support_id']}
        support_dict.update({'_id':support_dict['support_id']})
        cls.coll.update(filter, support_dict, upsert=True, j=True)
    
    @classmethod
    @mongo_exception
    def delete_support_by_id(cls,support_id):
        """删除服务支持"""
        cls.coll.remove({"_id":support_id})

    @classmethod
    @mongo_exception
    def get_all_supports_list(cls):
        supports = cls.coll.find()
        support_list = [support for support in supports]
        return support_list

    @classmethod
    @mongo_exception
    def get_supports_by_nick(cls, nick):
        supports = cls.coll.find({'nick':nick})
        support_list = [support for support in supports]
        return support_list
    
    
    @classmethod
    @mongo_exception
    def get_supports_by_key(cls, key, value):
        supports = cls.coll.find({key:value})
        support_list = [support for support in supports]
        return support_list
    
    @classmethod
    @mongo_exception
    def get_supports_between_time(cls, start_time, end_time):
        supports = cls.coll.find({'service_time':{'$gte':start_time, '$lte':end_time}})
        support_list = [support for support in supports]
        return support_list
        
    @classmethod
    @mongo_exception
    def get_mark_support_by_worker(cls,worker_id):
        filter={"worker_id":worker_id,"is_mark":True}
        cursour=cls.coll.find(filter)
        return [support for support in cursour]

    @classmethod
    @mongo_exception
    def get_supports_dynamic(cls,filter):
        print filter
        cursour=cls.coll.find(filter)
        supports=[support for support in cursour]
        return supports
