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

class Status(object):
    """卖家状态信息 """
    
    _conn = settings.user_conn 
    coll = _conn['user_center']['status']


    @classmethod
    def _get_id(cls,sid,article_code):
        """获取_id,_id由sid+article_code组成"""
        return "%s%s" %(int(sid),article_code.strip())
    
    @classmethod
    @mongo_exception
    def is_exists(cls,sid,article_code):
        """是否存在,_id:sid+article_code的字符串"""
        filter={"_id":cls._get_id(sid,article_code)}
        count = cls.coll.find(filter).count()
        if count > 0:
            return True
        return False

    @classmethod
    @mongo_exception
    def insert_shop_status(cls,shop_status_dict):
        """保存 shop status """
        key = cls._get_id(shop_status_dict["sid"],shop_status_dict["article_code"])
        shop_status_dict.update({"_id":key})
        cls.coll.save(shop_status_dict)
    
    @classmethod
    @mongo_exception
    def upset_shop_status(cls,shop_status_dict):
        key = cls._get_id(shop_status_dict["sid"],shop_status_dict["article_code"])
        filter={"_id":key}
        shop_status={}
        shop_status.update(shop_status_dict)
        if "_id" in shop_status:
            shop_status.pop("_id")
        cls.coll.update(filter,{"$set":shop_status},upsert=False)


    @classmethod
    @mongo_exception
    def upset_shop_deadline(cls,sid,article_code,order_cycle_end):
        """更新用户应用的到期时间"""
        key = cls._get_id(sid,article_code)
        filter = {"_id":key}
        update_dict = {"deadline":order_cycle_end}
        cls.coll.update(filter,{"$set":update_dict},upsert=False)
    
    @classmethod
    @mongo_exception
    def upset_shop_first_order_time(cls,sid,article_code,order_cycle_start):
        """更新用户应用的首次订购时间"""
        key = cls._get_id(sid,article_code)
        filter = {"_id":key}
        update_dict = {"first_order_time":order_cycle_start}
        cls.coll.update(filter,{"$set":update_dict},upsert=False)

    @classmethod
    @mongo_exception
    def upsert_active_by_sid(cls,sid,article_code,is_active):
        """更新用户的活跃状态标记"""
        key = cls._get_id(sid,article_code)
        filter = {"_id":key}
        update_dict = {"is_active":is_active}
        cls.coll.update(filter,{"$set":update_dict},upsert=False)

    @classmethod
    @mongo_exception
    def upset_user_status_by_sid(cls,sid,article_code,user_status,msg = None):
        """更新用户的效果态标记"""
        key = cls._get_id(sid,article_code)
        filter = {"_id":key}
        update_dict = {"user_status":user_status,"status_mark_time":datetime.combine(datetime.now(),dt.time()),"msg":msg}
        cls.coll.update(filter,{"$set":update_dict},upsert=False)

    @classmethod
    @mongo_exception
    def get_shop_status_by_sid(cls,sid):
        filter={"sid":int(sid)}
        cursor = cls.coll.find(filter)
        return  [doc for doc in cursor]

    @classmethod
    @mongo_exception
    def get_shop_status(cls,sid,article_code):
        key = cls._get_id(sid,article_code)
        filter = {"_id":key}
        obj = cls.coll.find_one(filter)
        return obj

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
        filter = {"article_code":article_code}
        cursor = cls.coll.find(filter)
        return [doc for doc in cursor]

    @classmethod
    @mongo_exception
    def get_shop_status_by_dynamic(cls,filter,fields=None):
        """动态查询 shop status,fileds 为 None 或空查全部字段,fileds 列表不为空则查指定字段"""
        if fields is None or len(fields) ==0:
            cursor = cls.coll.find(filter)
        else:
            field_dict = {}.fromkeys(fields,1)
            cursor = cls.coll.find(filter,field_dict)
        return [doc for doc in cursor]

    @classmethod
    @mongo_exception
    def count_normal_allocated_shop(cls,worker_id,article_code ="ts-1796606"):
        """客服有效服务人数"""
        filter = {"article_code":article_code,"deadline":{"$gt":datetime.now()},"worker_id":worker_id}
        return cls.coll.find(filter).count()
