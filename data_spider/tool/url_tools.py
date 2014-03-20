#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-03-17 11:53
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""


def get_url_by_cat_id(cat_id,page_no):
    """根据类目id,获取该类目下的应用列表"""
    url = "http://fuwu.taobao.com/ser/list.htm?tab_cat_id=51052018&current=-1&is_multi_list=0&primary_sort_desc=true&cat_map_id=%s&tracelog=category&current_page=%s" % (cat_id,page_no)
    return url

def get_article_base_url_by_article_code(article_code):
    """应用详情页面"""
    url = "http://fuwu.taobao.com/ser/detail.htm?service_code=%s" %(article_code)
    return url

def get_isv_index_url(isv_id):
    """获取isv首页"""
    url ="http://fuwu.taobao.com/serv/shop_index.htm?isv_id=%s" %(isv_id)
    return url

def get_isv_article_list_url(isv_id,page_id):
    url = "http://fuwu.taobao.com/serv/shop_index.htm?page_id=%s&isv_id=%s&page_rank=2&tab_type=1" %(page_id,isv_id)
    return url

def get_orders_url_by_article_code(article_code,page_no):
    """应用详情页中的订购记录"""
    url = "http://fuwu.taobao.com/serv/rencSubscList.do?serviceCode=%s&currentPage=%s&pageCount=%s"%(article_code,page_no,page_no)
    return url

def get_suggests_url_by_article_code(article_code,page_no):
    """应用详情页中的评价记录"""
    url="http://fuwu.taobao.com/score/query_suggest.do?service_code=%s&currentPage=%s&fee=1&orderType=&callback=jsonp_reviews_list" %(article_code,page_no) 
    return url
