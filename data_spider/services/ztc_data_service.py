#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-03-14 15:29
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import random
import logging
import logging.config
import datetime as dt
from datetime import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
    from data_spider.conf import set_env
    set_env.getEnvReady()

from data_spider.parser.html_parser import HtmlParser
from data_spider.db_models.isv import Isv
from data_spider.db_models.article import Article
from data_spider.db_models.article_base import ArticleBase
from data_spider.db_models.sync_status import SyncStatus
from data_spider.db_models.article_order import ArticleOrder 
from data_spider.db_models.article_suggest import ArticleSuggest
from data_spider.tool.request_tools import get_response
from data_spider.tool.url_tools import get_url_by_cat_id,get_article_base_url_by_article_code,get_isv_index_url,get_isv_article_list_url,get_orders_url_by_article_code,get_suggests_url_by_article_code
logger = logging.getLogger(__name__)

class ZtcDataService(object):

    @classmethod
    def sync_article_by_cat(cls,cat_id,page_no = 1):
        """按照类目获取该类目下的isv以及article"""
        logger.debug("sync article and isv  cat_id:%s,page_no:%s" %(cat_id,page_no))
        url = get_url_by_cat_id(cat_id,page_no)
        html = get_response(url)
        data = HtmlParser.parse_article(html)
        if not data:
            return
        Isv.upsert_isv_list(data["isv_list"])
        Article.upsert_article_list(data["article_list"])
        if not data["is_page_end"]:
            next_page = data["current_page"]+1
            cls.sync_article_by_cat(cat_id,next_page)


    @classmethod
    def fetch_article_base_by_id(cls,article_code):
        """抓取artice基础数据"""
        logger.debug("sync article base article_code:%s" %(article_code))
        url = get_article_base_url_by_article_code(article_code)
        html =get_response(url)
        data = HtmlParser.parse_artice_base(html)
        return data


    @classmethod
    def fetch_orders_by_id(cls,article_code,page_no = 1):
        """获取应用订购记录"""
        logger.debug("fetch_orders_by_id  article_code:%s,page_no:%s" %(article_code,page_no))
        url = get_orders_url_by_article_code(article_code,page_no)
        html = get_response(url)
        data = HtmlParser.parse_orders(html)
        return data

    @classmethod
    def fetch_suggests_by_id(cls,article_code,page_no = 1):
        """获取应用评价记录"""
        logger.debug("fetch_suggests_by_id  article_code:%s,page_no:%s" %(article_code,page_no))
        url = get_suggests_url_by_article_code(article_code,page_no)
        html = get_response(url)
        data = HtmlParser.parse_suggests(html)
        return data

        
    @classmethod
    def sync_isv_article_by_isv(cls,isv_id,page_id = None,complete = True):
        """获取isv下的应用详情,此接口获取无cat_id"""
        if not  page_id:
            page_id = cls.get_isv_page_id_by_isv(isv_id) 
        if not page_id:
            logger.debug("sync_isv_article_by_isv page_id not found isv_id:%s" %(isv_id))
            return
        url = get_isv_article_list_url(isv_id,page_id)
        html = get_response(url)
        data = HtmlParser.parse_isv_article(html)
        if data:
            article_base_list = data["article_base_list"]
            article_list = data["article_list"]
            base_dict = dict((obj["article_code"],obj) for obj in article_base_list)
            article_dict = dict((obj["article_code"],obj) for obj in article_list)
            rpt_date = datetime.combine(datetime.now(),dt.time())
            for article_code,article in article_dict.iteritems():
                article_base = base_dict[article_code]
                new_article_base = None
                if complete:
                    new_article_base = cls.fetch_article_base_by_id(article_code)
                is_exist = Article.is_exist(article["article_code"])
                if not is_exist:
                    if new_article_base:
                        article["cat_id"] = new_article_base["cat_id"]
                    article["isv_id"] = isv_id 
                    Article.insert_article(article)

                article_base["rpt_date"] = rpt_date
                article_base["isv_id"] = isv_id 
                if new_article_base:
                    if "cat_id" in new_article_base:
                        new_article_base.pop("cat_id")
                    article_base.update(new_article_base)
                is_exist = ArticleBase.is_exist(article_base["article_code"],rpt_date)
                if not is_exist:
                    ArticleBase.insert_article_base(article_base)
                else:
                    ArticleBase.upset_article_base(article_base)


    @classmethod
    def sync_orders_by_id(cls,article_code):
        """抓取订购记录"""
        page_no = 1
        page_count =15
        sync_status = SyncStatus.get_sync_status_by_id(article_code)
        ignore_minute = 3
        sync_order_time = datetime.now() - dt.timedelta(minutes=ignore_minute)
        flag = True
        while page_no < page_count and flag:
            data = cls.fetch_orders_by_id(article_code,page_no)
            if not data:
                logger.info("sync_orders_by_id can't get orders article_code:%s" %(article_code))
                flag = False
                return 
            page_count = data["pageCount"]
            order_list = []
            page_no +=  1
            for order in data["data"]:
                order["article_code"] = article_code
                pay_time = order["payTime"]
                if pay_time > datetime.now() - dt.timedelta(minutes = ignore_minute - 1):
                    continue
                if not sync_status or "sync_order_time" not in sync_status or sync_status["sync_order_time"] < pay_time:
                    order_list.append(order)
                else:
                    flag = False
                    break
            ArticleOrder.upsert_article_order_list(order_list)
        update_dict = {"article_code":article_code,"sync_order_time":sync_order_time} 
        if sync_status is None:
            SyncStatus.insert_sync_status(update_dict)
        else:
            SyncStatus.upset_sync_status(update_dict)

    @classmethod
    def sync_suggests_by_id(cls,article_code,max_page = None):
        """抓取评价"""
        page_no = 1
        page_count =15
        sync_status = SyncStatus.get_sync_status_by_id(article_code)
        ignore_minute = 3
        sync_suggest_time = datetime.now() - dt.timedelta(minutes=ignore_minute)
        flag = True
        while page_no < page_count and flag:
            if max_page and page_no > max_page:
                logger.info("sync_suggests_by_id needn't get more suggest article_code:%s, max_page:%s" %(article_code,max_page))
                flag = False
                break
            data = cls.fetch_suggests_by_id(article_code,page_no)
            if not data or not data["success"]:
                logger.info("sync_suggests_by_id can't get suggests article_code:%s" %(article_code))
                flag = False
                return 
            page_count = data["totalPage"]
            suggest_list = []
            page_no +=  1
            for suggest in data["comments"]:
                gmt_create = suggest["gmtCreate"]
                gmt_modified = suggest["gmtModified"]
                if not sync_status or "sync_suggest_time" not in sync_status  or sync_status["sync_suggest_time"] < gmt_create or sync_status["sync_suggest_time"] < gmt_modified:
                    suggest_list.append(suggest)
                else:
                    flag = False
                    break
            ArticleSuggest.upsert_article_suggest_list(suggest_list)
        update_dict = {"article_code":article_code,"sync_suggest_time":sync_suggest_time} 
        if sync_status is None:
            SyncStatus.insert_sync_status(update_dict)
        else:
            SyncStatus.upset_sync_status(update_dict)

    @classmethod
    def get_isv_page_id_by_isv(cls,isv_id):
        logger.debug("get isv page_id:%s" %(isv_id))
        url = get_isv_index_url(isv_id)
        html = get_response(url)
        page_id = HtmlParser.parse_isv_id(html)
        return page_id
    
if __name__ == "__main__":
    article_code = "ts-1796606"
    article_code = "appstore-9092"
    #ZtcDataService.sync_article_by_cat(51052018)
    #ZtcDataService.fetch_article_base_by_id("ts-1796606")
    #ZtcDataService.get_isv_page_id_by_isv("847721042")
    #ZtcDataService.sync_isv_article_by_isv("847721042")
    #ZtcDataService.fetch_orders_by_id(article_code)
    ZtcDataService.sync_orders_by_id(article_code)
    ZtcDataService.sync_suggests_by_id(article_code)
