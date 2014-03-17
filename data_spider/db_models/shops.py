#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'


import sys
import os
import logging
import logging.config
from datetime import  datetime
import datetime as dt


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))

from user_center.conf import settings 
from user_center.common.decorator import  mongo_exception

class Shops(object):
    """
    class to operate shop_info collections
    """

    _conn = settings.user_conn
    coll = _conn['user_center']['shops']


    @classmethod
    @mongo_exception
    def is_shop_exist(cls,nick):
        shop = cls.coll.find_one({'_id':nick})
        if shop is None:
            return False
        else:
            return True

    @classmethod
    @mongo_exception
    def upset_shop(cls,shop_dict):
        filter = {'_id':shop_dict['nick']}
        if shop_dict.has_key('_id'):
            del shop_dict['_id']
        cls.coll.update(filter, {'$set':shop_dict}, upsert=False)

    @classmethod
    @mongo_exception
    def upsert_shop(cls,shop_dict):
        filter = {'_id':shop_dict['nick']}
        shop_dict.update({'_id':shop_dict['nick']})
        cls.coll.update(filter, shop_dict, upsert=True, j=True)
    
    @classmethod
    @mongo_exception
    def get_all_shop_list(cls):
        shops = cls.coll.find()
        shop_list = [shop for shop in shops]
        return shop_list

    @classmethod
    @mongo_exception
    def get_shop_by_sid(cls,shop_id):
        shop = cls.coll.find_one({'sid':shop_id})
        return shop

    @classmethod
    @mongo_exception
    def get_shop_by_nick(cls, nick):
        shop = cls.coll.find_one({'_id':nick})
        return shop
    
    @classmethod
    @mongo_exception
    def count_normal_allocated_shop(cls, worker_id):
        num = cls.coll.find({'worker_id':worker_id, 'flag':True}).count()
        return num

    @classmethod
    @mongo_exception
    def count_today_allocated(cls,worker_id):
        today = datetime.combine(datetime.now(),dt.time())
        num = cls.coll.find({'worker_id':worker_id, 'allocate_time':today}).count()
        return num
    
    @classmethod
    @mongo_exception
    def get_shops_by_key(cls, key, value):
        shops = cls.coll.find({key:value})
        shop_list = [shop for shop in shops]
        return shop_list

