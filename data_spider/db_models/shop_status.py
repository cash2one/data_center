#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2013-08-07 11:37
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import datetime as dt
from datetime import  datetime
from user_center.conf import settings 
from user_center.common.decorator import mongo_exception

class ShopStatus(object):
    """卖家状态信息 """
    
    _conn = settings.user_conn 
    coll = _conn['user_center']['shop_status']


    @classmethod
    @mongo_exception
    def is_exists(cls,sid):
        """是否存在"""
        filter={"_id":int(sid)}
        shop_status = cls.coll.find_one(filter)
        if shop_status is not None:
            return True
        return False
        
    @classmethod
    @mongo_exception
    def upsert_shop_status(cls,shop_status_dict):
        filter={"_id":int(shop_status_dict["sid"])}
        shop_status={}
        shop_status.update(shop_status_dict)
        if "_id" in shop_status:
            shop_status.pop("_id")
        cls.coll.update(filter,{"$set":shop_status},upsert=True)
    
    @classmethod
    @mongo_exception
    def update_shop_status(cls,shop_status_dict):
        filter={"_id":int(shop_status_dict["sid"])}
        shop_status={}
        shop_status.update(shop_status_dict)
        if "_id" in shop_status:
            shop_status.pop("_id")
        cls.coll.update(filter,{"$set":shop_status},upsert=False)

    @classmethod
    @mongo_exception
    def upset_shop_deadline(cls,sid,article_code,order_cycle_end):
        """更新用户应用的到期时间"""
        deadline_key ="deadline.%s" % (article_code)
        update_dict = {deadline_key:order_cycle_end}
        cls.coll.update({"_id":int(sid)},{"$set":update_dict},upsert=False)
    
    @classmethod
    @mongo_exception
    def upset_shop_first_order_time(cls,sid,article_code,order_cycle_start):
        """更新用户应用的到期时间"""
        first_order_time_key ="first_order_time.%s" % (article_code)
        update_dict = {first_order_time_key:order_cycle_start}
        cls.coll.update({"_id":int(sid)},{"$set":update_dict},upsert=False)

    @classmethod
    @mongo_exception
    def upsert_active_by_sid(cls,sid,active_dict):
        """更新用户的活跃状态标记"""
        article_dict={"is_active":active_dict["is_active"],"update_time":datetime.now()}
        active_key ="active.%s" % (active_dict["article_code"])
        campaign_status_dict = active_dict["campaign_status"]
        campaign_status_dict["update_time"] = datetime.combine(datetime.now(),dt.time())
        campaign_status_key = "campaign_status.%s" %(active_dict["article_code"])

        update_dict = {"sid":int(sid),"nick":active_dict["nick"],active_key:article_dict,campaign_status_key:campaign_status_dict}
        cls.coll.update({"_id":int(sid)},{"$set":update_dict},upsert=True)

    @classmethod
    @mongo_exception
    def upset_user_status_by_sid(cls,sid,article_code,user_status,msg = None):
        """更新用户的效果态标记"""
        article_dict={"status":user_status,"status_mark_time":datetime.combine(datetime.now(),dt.time()),"msg":msg}
        active_key ="user_status.%s" % (article_code)

        update_dict = {active_key:article_dict}
        cls.coll.update({"_id":int(sid)},{"$set":update_dict},upsert=False)

    @classmethod
    @mongo_exception
    def get_shop_status_by_sid(cls,sid):
        filter={"_id":int(sid)}
        return cls.coll.find_one(filter)

    @classmethod
    @mongo_exception
    def get_shop_status_list(cls):
        """查找所有的shop status """
        cursor = cls.coll.find()
        return [doc for doc in cursor]

    @classmethod
    @mongo_exception
    def get_shop_status_by_article_code(cls,article_code):
        """根据article_code 查找以及订购用的 shop status"""
        key = "deadline.%s" %(article_code)
        filter = {key:{"$exists":1}}
        cursor = cls.coll.find(filter)
        return [doc for doc in cursor]

    @classmethod
    @mongo_exception
    def get_shop_status_by_dynamic(cls,filter):
        """动态查询 shop status"""
        cursor = cls.coll.find(filter)
        return [doc for doc in cursor]
