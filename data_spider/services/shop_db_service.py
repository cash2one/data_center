# -*- coding: utf-8 -*-
"""
@author:  zhoujiebing
@contact: zhoujiebing@maimiaotech.com
@date: 2013-05-02 16:18
@version: 0.0.0
@license: Copyright maimiaotech.com
@copyright: Copyright maimiaotech.com

"""

import sys
import os
from datetime import datetime,timedelta
import random
import logging
import logging.config
import datetime as dt
from time import sleep

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
    from user_center.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from tao_models.conf.settings import set_taobao_client
from tao_models.taobao_shop_get import ShopGet
from tao_models.items_onsale_get import ItemsOnsaleGet
from user_center.conf.settings import WORKER_DICT, FULL_NUM, ARTICLE_LIST,STATUS_ARTICLE_LIST,WORKER_ID_XUQIAN,WORKER_ID_VIP
from user_center.db_models.shops import Shops
from user_center.db_models.orders import Orders 
from user_center.db_models.status import Status
from user_center.db_models.rpt_worker_active import RptWorkerActive
from user_center.tool.seller_info_tool import SellerInTool
from user_center.tool.appkey_tools import  set_appkey
from user_center.tool.worker_tool import  allocate_worker_id,build_rate_dict
from user_center.tool.order_tools import get_order_count,renew_status,merge_orders,get_first_conitnue_use_order
logger = logging.getLogger(__name__)

class ShopDBService(object):
    """用户信息中心
    _id:nick
    nick
    sid
    worker_id 专属客服id
    update_time
    flag 标识是否为有效用户
    seller_name
    seller_mobile
    seller_email
    article_order_id 某个article对应的order_id
    article_status 某个article的状态
    article_deadline 某个article的到期时间
    """

    @classmethod
    def is_shop_exist(cls, nick):
        """判断是否存在该shop"""

        return Shops.is_shop_exist(nick)

    @classmethod
    def upset_shop(cls, shop_dict):
        """全量更新shop信息"""

        return Shops.upset_shop(shop_dict)
    
    @classmethod
    def upsert_shop(cls, shop_dict):
        """更新shop信息"""
        
        Shops.upsert_shop(shop_dict)
    
    @classmethod
    def upset_worker_id(cls, nick, worker_id):
        """更新worker_id"""

        shop = Shops.get_shop_by_nick(nick)
        if not shop:
            return False
        shop['worker_id'] = worker_id
        Shops.upset_shop(shop)
        return True

    @classmethod
    def get_shop_by_sid(cls, shop_id):
        """根据sid获取shop_info"""

        return Shops.get_shop_by_sid(shop_id)

    @classmethod
    def get_shop_by_nick(cls, nick):
        """根据nick获取shop_info"""

        return Shops.get_shop_by_nick(nick)
    
    @classmethod
    def get_all_shop_list(cls):
        """ 获取所有shop_info"""
        
        return Shops.get_all_shop_list()

    @classmethod
    def get_shops_by_key(cls, key, value):
        """根据某些key获取shop_list"""

        return Shops.get_shops_by_key(key, value)
    
    @classmethod
    def get_shops_by_artice_code(cls,article_code,search_expire = False):
        """查找订购了该应用的用户,search_expire = True 时过期的用户也会查找出来"""
        shop_list = Shops.get_all_shop_list()
        return shop_list

    @classmethod
    def count_normal_allocated_shop(cls, worker_id):
        """统计某个客服已分配到的有效客户数"""

        return Status.count_normal_allocated_shop(worker_id)

    @classmethod
    def get_shop_status(cls,nick,article_code):
        """获取单个shop status 建议使用get_shop_status_by_sid 方法更快一点"""
        shop = Shops.get_shop_by_nick(nick)
        if shop and "sid" in shop:
            return Status.get_shop_status(shop["sid"],article_code)

    @classmethod
    def get_shop_status_by_sid(cls,sid,article_code):
        return Status.get_shop_status(sid,article_code)

    @classmethod
    def allocate_one_shop(cls,nick):
        """
        按照客服的活跃率分配客服
        1-2名:20%
        3-7名:12%
        8名:0%
        """
        if 1==1:
            if type(nick) == str:
                nick = nick.decode("utf-8")
            #临时设置为新分配则都为公共客服
            worker_id_list_1 = WORKER_ID_XUQIAN 
            worker_id_list_2 = WORKER_ID_VIP
            orders = Orders.get_orders_by_nick(nick)
            bd_order_num = len([order for order in orders if order["article_code"] == "ts-1797607"])
            worker_id_xuqian = sorted(worker_id_list_1)[abs(hash(nick)%len(worker_id_list_1))]
            worker_id_vip = sorted(worker_id_list_2)[abs(hash(nick)%len(worker_id_list_2))]
            if bd_order_num >0:
                return (worker_id_vip,worker_id_vip,worker_id_vip)
            order_list = filter(lambda order:order["article_code"] == "ts-1796606",orders)
            pay_count,renew_count= get_order_count(order_list)
            if renew_count >0:
                return (worker_id_vip,worker_id_xuqian,worker_id_vip)
            else:
                return (worker_id_xuqian,worker_id_xuqian,worker_id_vip)


        rpt_list = RptWorkerActive.get_rpt_latest()
        worker_rpt_dict ={}
        a= 0.00000001
        ingore_list=[9,-1,-2,None]
        
        full_set = set()
        less_set = set()
        over_set = set()
        for worker_id in WORKER_DICT.keys():
            service_num = Shops.count_normal_allocated_shop(worker_id)
            if service_num >= FULL_NUM: 
                full_set.add(worker_id)
            else:
                if service_num <2000:
                    less_set.add(worker_id)
                today_num = Shops.count_today_allocated(worker_id)
                if today_num >=150:
                    over_set.add(worker_id)
        for rpt in  rpt_list:
            worker_id = rpt["worker_id"]
            if worker_id in ingore_list:
                continue
            if worker_id in full_set: #服务数过多则不再分配客户
                continue
            if worker_id not in worker_rpt_dict:
                active_rate = rpt["active_num"]/(rpt["total"]+a)
                worker_rpt_dict[worker_id] = {"worker_id":worker_id,"active_rate":active_rate,"total":rpt["total"],"active_num":rpt["active_num"]} 
            else:
                active_rate =(rpt["active_num"] + worker_rpt_dict[worker_id]["active_num"]) /(worker_rpt_dict[worker_id]["total"] + rpt["total"]+a)
                worker_rpt_dict[worker_id]["active_rate"] =active_rate
                worker_rpt_dict[worker_id]["active_num"] += rpt["active_num"]
                worker_rpt_dict[worker_id]["total"] += rpt["total"]
        worker_rpt_list = worker_rpt_dict.values()
        worker_rpt_list.sort(key=lambda e:e["active_rate"],reverse=True)
        worker_num ={}
        size = len(worker_rpt_list)
        if size ==0:
            return None 
        elif size ==1:
            return worker_rpt_list[0]["worker_id"]
        worker_range =([2,20],[7,11],[8,5])
        worker_ids = [rpt["worker_id"] for rpt in worker_rpt_list]
        rate_dict = build_rate_dict(worker_ids,worker_range)
        for i in range(3):
            rand_num = random.randint(1, 10000000) % 100 + 1
            temp = {}
            temp.update(rate_dict)
            #import pdb;pdb.set_trace()
            for strong_id in [121,11]:
                if strong_id not in rate_dict and strong_id in less_set:
                    temp.update({strong_id:30})
            if len(temp) != len(rate_dict):
                rand_num = random.randint(1, 10000000) % sum(temp.values()) + 1
            worker_id = allocate_worker_id(rand_num,temp)
            if worker_id in less_set and worker_id not in over_set:
                return worker_id

        for i in range(3):
            rand_num = random.randint(1, 10000000) % 100 + 1
            worker_id = allocate_worker_id(rand_num,rate_dict)
            if worker_id is not None and worker_id not in over_set:
                return worker_id
        return None
    
    @classmethod
    def store_shop_to_center(cls,nick, sid, access_token,article_code, deadline):
        """存储用户数据到用户中心,注意taobao_client 不同将导致环境设置,以及并发问题"""
        upsert_flag = False
        exist_flag=True
        shop = cls.get_shop_by_nick(nick)
        if not shop:
            shop = {'nick':str(nick), 'sid':int(sid)}
            exist_flag=False
        
        if not shop or not shop.get('worker_id'):
            worker_id ,worker_id_xuqian,worker_id_vip = cls.allocate_one_shop(nick)
            logger.info("allocate_id nick:%s,worker_id:%s" %(nick,worker_id))
            shop['worker_id'] = worker_id
            shop['worker_id_xuqian'] = worker_id_xuqian
            shop['worker_id_vip'] = worker_id_vip
            shop['allocate_time'] = datetime.combine(datetime.now(),dt.time())
            upsert_flag = True
        
        need_call_seller_api=not shop.get('seller_mobile', None) or not shop.get("level",None) or not shop.get("city",None) 
        need_call_cid_api= not shop.get('cid',None) 
        need_call_item_api= shop.get('item_count',0)==0
        if need_call_seller_api or need_call_cid_api or need_call_item_api:
            upsert_flag = True
            set_appkey(article_code)
            if need_call_cid_api:
                shop_taobao=ShopGet.get_shop(nick,access_token)
                if shop_taobao is not None:
                    shop_dict=shop_taobao.toDict()
                    shop['cid']=shop_dict.get('cid','')
                    shop['pic_path']=shop_dict.get('pic_path','')
                    shop['shop_create']=shop_dict.get('created','')
            if need_call_item_api:
                onsale_dict=ItemsOnsaleGet.get_item_list_with_overview(access_token)
                if onsale_dict is not None:
                    shop['item_count']=onsale_dict.get('total_results',0)
            if need_call_seller_api:
                seller = SellerInTool.get_seller_info( access_token)
                if seller:
                    shop['seller_mobile'] = seller.get('seller_mobile', '')
                    shop['seller_phone'] = seller.get('seller_phone', '')
                    shop['seller_name'] = seller.get('seller_name', '')
                    shop['seller_email'] = seller.get('seller_email', '')
                    shop['sex']=seller.get('sex','')
                    shop['is_golden_seller']=seller.get('is_golden_seller',False)
                    shop['consumer_protection']=seller.get('consumer_protection',False)
                    #shop['promoted_type']=seller.get('promoted_type',False)
                    shop['user_id']=seller.get('user_id',-1)
                    shop['seller_name']=seller.get('seller_name','')
                    shop['auto_repost']=seller.get('auto_repost','')
                    shop['avatar']=seller.get('avatar','')
                    shop['type']=seller.get('type','C')
                    seller_credit=seller.get('seller_credit',None)
                    if seller_credit is not None:
                        shop['level']=seller_credit.get('level',-1)
                        shop['total_num']=seller_credit.get('total_num',0)
                        shop['good_num']=seller_credit.get('good_num',0)
                    address_list=seller.get('address',None)
                    if address_list is not None:
                        for address in address_list:
                            if address['get_def']:
                                if ''==shop['seller_mobile']: 
                                    shop['seller_mobile']=address.get('mobile_phone','')
                                shop['province']=address.get('province','')
                                shop['city']=address.get('city','')
                                shop['country']=address.get('country','')
                                break

        if upsert_flag:
            shop['flag'] = True
            time_now = datetime.now()
            shop['update_time'] = time_now
            if exist_flag:
                cls.upset_shop(shop)
            else:
                cls.upsert_shop(shop)
        cls.store_order_status(nick,sid)

    @classmethod
    def store_order_status(cls,nick,sid,order_list = None):
        """保存首次订购,到期时间,续费次数"""
        if order_list is None:
            order_list = Orders.get_orders_by_nick(nick)
        order_list.sort(key = lambda e:e["order_cycle_end"],reverse = True)
        order_dict = {}
        for order in order_list:
            if order["article_code"] not in order_dict:
                order_dict[order["article_code"]] = []
            order_dict[order["article_code"]].append(order)
        for article_code ,order_list in order_dict.iteritems():
            if article_code not in STATUS_ARTICLE_LIST:
                continue
            order_list.sort(key = lambda e:e["order_cycle_end"])
            if len(order_list) > 0:
                deadline_new = order_list[-1]["order_cycle_end"]
                first_order_time = order_list[0]["create"]
                pay_count,renew_count= get_order_count(order_list)
                merge_order_list = merge_orders(order_list)
                is_new,order_cycle = renew_status(merge_order_list)
                first_last_order = get_first_conitnue_use_order(merge_order_list)
                continue_use_create =first_last_order["create"]
                continue_use_start =first_last_order["order_cycle_start"]

                status  = Status.get_shop_status(sid,article_code)
                if status is None:
                    shop = Shops.get_shop_by_nick(nick)
                    worker_id = None
                    if shop is not None:
                        worker_id = shop.get("worker_id")

                    status_dict = {"sid":sid,"nick":nick,"article_code":article_code,"worker_id":worker_id,"pay_count":pay_count,"renew_count":renew_count}
                    status_dict["user_status"] = "good"
                    status_dict["deal_status"] = "undeal"
                    status_dict["status_mark_time"] = datetime.combine(datetime.now(),dt.time())
                    status_dict["first_order_time"] = first_order_time
                    status_dict["deadline"] = deadline_new
                    status_dict["msg"] = None 
                    status_dict["is_new"] = is_new
                    status_dict["order_cycle"] = order_cycle
                    status_dict["continue_use_create"] = continue_use_create 
                    status_dict["continue_use_start"] = continue_use_start
                    Status.insert_shop_status(status_dict)
                else:
                    status_dict = {"sid":sid,"article_code":article_code,"pay_count":pay_count,"renew_count":renew_count,"first_order_time":first_order_time,"deadline":deadline_new,"is_new":is_new,"order_cycle":order_cycle,"continue_use_create":continue_use_create,"continue_use_start":continue_use_start}
                    if status.get("worker_id",None) is None:
                        shop = Shops.get_shop_by_nick(nick)
                        if shop is not None:
                            worker_id = shop.get("worker_id")
                            status_dict["worker_id"] = worker_id
                    Status.upset_shop_status(status_dict)


if __name__ == '__main__':
    nick = 'chinchinstyle'
    worker_id = 1
    #ShopDBService.upset_worker_id(nick, worker_id)
    #ShopDBService.store_shop_to_center("麦苗科技001", 101240238, "6201d27bf053e7b95eabeb7fb9f46397ce5ZZ32c186caa1871727117","ts-1796606", None)
    ShopDBService.store_shop_to_center("麦苗科技001", 101240238, "62001001ZZ38431ae2ef7018e141da64620191d6a7ccadb871727117","ts-1797607", None)
    ShopDBService.store_order_status("luoidtaobao",59788011)
