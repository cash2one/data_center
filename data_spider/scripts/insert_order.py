#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zhoujiebin
@contact: zhoujiebing@maimiaotech.com
@date: 2012-12-10 17:13
@version: 0.0.0
@license: Copyright maimiaotech.com
@copyright: Copyright maimiaotech.com

"""
import os
import sys
import time
import logging,logging.config
if __name__ == '__main__':
    curr=os.path.normpath(os.path.dirname(__file__))
    log_path=os.path.normpath(os.path.join(curr,'../conf/log4p_file_console.conf'))
    sys.path.append(os.path.normpath(os.path.join(curr,'../../')))
    logging.config.fileConfig(log_path)
import datetime
import user_center.conf.settings
from user_center.services.order_db_service import OrderDBService
from tao_models.conf.settings import set_taobao_client
set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')
from tao_models.vas_order_search import VasOrderSearch
from user_center.db_models.app import App
from user_center.tool.send_tools import send_sms,send_email_with_text,DIRECTOR
logger=logging.getLogger(__file__)

class UserOrder:

    def __init__(self, article_code):
        self.article_code = article_code
        #self.code_name = {'ts-1796606':'省油宝'}
        self.code_name = {'ts-1796606':'省油宝', 'ts-1797607':'选词王', 'ts-1817244':'淘词'}
        self.order_type = {1:'新订', 2:'续订', 3:'升级', 4:'后台赠送', 5:'后台自动续订', 6:'订单审核后生成订购关系'}

    def get_lost_order(self, start_created, end_created):
        """获取某段时间的订单
        date 是datetime.datetime(2013,2,18,0,0,0) 这种类型"""
        self.order_list = VasOrderSearch.search_vas_order(self.article_code, start_created, end_created)
        print 'len order_list: ', len(self.order_list)

    def get_yesterday_order(self):
        """获取昨天的订单"""

        self.order_list = VasOrderSearch.search_vas_order_yesterday(self.article_code)
        print 'len order_list: ', len(self.order_list)

    def get_order_by_time(self, start_time, end_time):
        """获取某段时间的订单
           start_time ,end_time 为 "%Y-%m-%d %H:%M:%S"格式的字符串
        """
        self.order_list = VasOrderSearch.search_vas_order(self.article_code, start_time, end_time)
        logger.info("[article_code:%s][start_time:%s][end_time:%s] 订购总数:%s" %(self.article_code,start_time,end_time, len(self.order_list)))

    def insert_order(self, date):
        """写入db date 是datetime.date类型"""

        app_name = self.code_name[self.article_code] 
        date = datetime.datetime.combine(date, datetime.time())
        for order in self.order_list:
            order_dict = order.toDict()
            order_dict['occur_time'] = date
            OrderDBService.upsert_order(order_dict)

    def check_order(self,start_time,end_time,check_db=False):
        """校验订单,由于带有时分秒时订单获取的api正确率更低,所以特殊处理校验前一日订单"""
        s= start_time.strftime("%Y-%m-%d %H:%M:%S")
        e= end_time.strftime("%Y-%m-%d %H:%M:%S")
        if "00:00:00" in s or "00:00:00" in e:
            order_count_real=VasOrderSearch.get_var_orders_count(self.article_code,start_time.strftime("%Y-%m-%d"),end_time.strftime("%Y-%m-%d"))
        else:
            order_count_real=VasOrderSearch.get_var_orders_count(self.article_code,s,e)
        order_count=len(self.order_list)
        if check_db:
            order_count=OrderDBService.get_orders_count(start_time,end_time,self.article_code)
        if order_count_real==order_count:
            message="[article_code:%s][start_time:%s][end_time:%s]订单数:%s 数据完整"\
                    %(self.article_code,s,e,order_count_real)
            logger.info(message)
            return None
        if order_count_real>order_count:
            self.get_order_by_time(s, e)
            self.insert_order(datetime.date.today())
            order_count_2=OrderDBService.get_orders_count(start_time,end_time,self.article_code)
            if order_count_real==order_count_2:
                logger.info("[article_code:%s][start_time:%s][end_time:%s]实际订购:%s 漏单已修复"\
                        %(self.article_code,start_time,end_time,order_count_real))
            else:
                message="[article_code:%s][start_time:%s][end_time:%s]实际订购:%s 数据库记录数:%s"\
                        %(self.article_code,start_time,end_time,order_count_real,order_count_2)
                logger.error(message)
                send_sms(DIRECTOR["PHONE"],message)

def insert_lost_order(start_date, end_date):
    """插入遗漏的订单"""

    while start_date <= end_date:
        start_created = datetime.datetime.combine(start_date, datetime.time())
        syb = UserOrder('ts-1796606')
        syb.get_lost_order(start_created, start_created+datetime.timedelta(days=1))
        syb.insert_order(start_created)
        xcw = UserOrder('ts-1797607')
        xcw.get_lost_order(start_created, start_created+datetime.timedelta(days=1))
        xcw.insert_order(start_created)
        print '抓取 ' + str(start_date) + '的订单成功'
        start_date += datetime.timedelta(days=1)
        time.sleep(30)

def insert_yesterday_order():
    """插入昨天的订单到数据库"""

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    syb = UserOrder('ts-1796606')
    syb.get_yesterday_order()
    syb.insert_order(yesterday)
    xcw = UserOrder('ts-1797607')
    xcw.get_yesterday_order()
    xcw.insert_order(yesterday)

def insert_order_by_time(article_code,start_time,end_time):
    """按应用id 获取指定时间段内的订购记录 """
    user_order=UserOrder(article_code)
    if article_code not in user_order.code_name:
        logger.info("article_code:%s 不存在,输入正确的应用id后再执行")
        return None
    s=start_time.strftime("%Y-%m-%d %H:%M:%d")
    e=end_time.strftime("%Y-%m-%d %H:%M:%d")
    user_order.get_order_by_time(s,e)
    d = datetime.date.today()
    user_order.insert_order(d)
    end_check_time=start_time -datetime.timedelta(hours=3)
    start_check_time=end_check_time - datetime.timedelta(hours=5)
    if 8<=datetime.datetime.now().hour<=9:
        #为防止api获取的总数本来就是错误的,所以加大验证昨日订单次数
        end_check_time=datetime.datetime.combine(datetime.date.today(),datetime.time())
        start_check_time=end_check_time - datetime.timedelta(days=1)
    user_order.check_order(start_check_time,end_check_time,check_db=True)
    

def insert_order_increment():
    """从应用上次获取订购记录的时间开始获取到现在的订购记录 """
    all_app=UserOrder(None) 
    for app_id,app_name in all_app.code_name.iteritems():
        app_syb=App.get_app_by_app_id(app_id)
        syb=UserOrder(app_id)
        if app_syb is None:
            gmt_last_sync=datetime.datetime.combine(datetime.datetime.today(),datetime.time())-datetime.timedelta(30)
            app_syb={"app_id":app_id,"app_name":syb.code_name[app_id],"gmt_last_sync":gmt_last_sync}
        e=datetime.datetime.now()-datetime.timedelta(minutes=15)
        s=app_syb['gmt_last_sync']-datetime.timedelta(hours=2)
        if s>e:
            continue
        insert_order_by_time(app_id,s,e)
        app_syb["gmt_last_sync"]=e
        App.upsert_app(app_syb)


if __name__ == '__main__':
    #insert_lost_order(datetime.date(2012, 11, 14), datetime.date(2012, 12, 31))
    #insert_yesterday_order()
    insert_order_increment()
