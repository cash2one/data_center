#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2013-08-04 21:15
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import os
import sys
from user_center.conf import settings 
from user_center.common.decorator import mongo_exception

class RptWorkerActive(object):
    """专属客服活跃度统计 """
    _conn=settings.user_conn
    coll=_conn["user_center"]["rpt_worker_active"]

    @classmethod
    @mongo_exception
    def upsert_rpt_worker_active(cls,rpt):
        filter={"rpt_date":rpt["rpt_date"],"worker_id":rpt["worker_id"]}
        cls.coll.update(filter,rpt,upsert=True,j=True)


    @classmethod
    @mongo_exception
    def get_rpt_worker_active(cls,start_date,end_date):
        filter={"rpt_date":{"$gte":start_date,"$lte":end_date}}
        cursor=cls.coll.find(filter)
        return [doc for doc in cursor]

    @classmethod
    @mongo_exception
    def get_rpt_latest(cls):
        """获取最新的活跃度统计报表"""
        cursor=cls.coll.find({}).sort("rpt_date",-1).limit(1)
        rpt_list =[doc for doc in cursor]
        rpt_latest = None
        if len(rpt_list) >0:
            rpt_latest = rpt_list[0]
        if rpt_latest is None:
            return []
        else:
            rpt_date = rpt_latest["rpt_date"]
            return cls.get_rpt_worker_active(rpt_date,rpt_date)

    @classmethod
    @mongo_exception
    def get_rpt_product_latest(cls):
        """获取最新的产品分析报表"""
        cursor=cls.coll.find({}).sort("rpt_date",-1).limit(1)
        rpt_list =[doc for doc in cursor]
        if len(rpt_list)==0:
            return None
        return rpt_list[0]

