#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-03-14 16:01
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import logging
import re
import urllib
import simplejson as json
from datetime import datetime
from HTMLParser import HTMLParser 
from BeautifulSoup import BeautifulSoup
logger = logging.getLogger(__name__)

class HtmlParser(object):
    

    _parser = HTMLParser()

    @classmethod
    def parse_article(cls,html):
        """article解析"""
        if not html or "J_Service" not in html:
            logger.info("parse_article not fond J_Service")
            return None
        if type(html) == type(""):
            html = html.encode("utf-8")
        soup = BeautifulSoup(html)
        container = soup.find(attrs ={"id":"J_Service"})
        #cat_id = soup.find(attrs={"id":"content"})["data-spm"]
        a_list = soup.find(attrs={"class":"crumb"}).findAll("a")
        cat_id = cls._parse_param("tab_cat_id",a_list[-1]["href"])
        article_obj_list = container.findAll("tr")
        current_page = int(soup.find(attrs={"id":"current_page"})["value"])
        is_page_end = soup.find(attrs={"class":"pagination"}).find(attrs={"class":"page-end"})

        article_list =[]
        isv_list = []
        for article_obj in article_obj_list:
            d1 = article_obj.find(attrs = {"class":"item-meta"})
            pic = d1.find("img")["src"]
            service_code = re.findall(r"service_code=(.+)&trace\w+",d1.find("a")["href"])[0]
            name = d1.find("h4").find("a")["title"]
            desc = cls._parser.unescape(d1.find("p",{"class":"desc"}).text)
            d2 = d1.find(attrs = {"class":"concat"}).find("a")
            isv_name = cls._parser.unescape(d2.text)
            isv_id =cls._parse_isv_id(d2["href"]) 

            score = article_obj.find("span",{"class":"ui-no-rate"})["title"]
            user_count = article_obj.findAll("td")[2].text
            price = article_obj.findAll("td")[3].find("p").text
            

            article = {"article_code":service_code,"pic":pic,"name":name,"isv_id":isv_id,"desc":desc,"cat_id":cat_id}
            isv = {"isv_id":isv_id,"name":isv_name}
            article_list.append(article)
            isv_list.append(isv)
        data = {"current_page":current_page,"is_page_end":is_page_end,"isv_list":isv_list,"article_list":article_list}
        return data 

    @classmethod
    def parse_artice_base(cls,html):
        """应用详情页中,解析应用的基本用户数据和评分"""
        if type(html) == type(""):
            html = html.encode("utf-8")
        if not html or "use-state" not in html:
            logger.info("parse_artice_base not fond use-state")
            return None
        soup = BeautifulSoup(html)
        score = soup.find(attrs={"class":"grade"}).text
        container = soup.find(attrs ={"class":"use-state"})
        num_objs = container.findAll("span",{"class":"count"})
        grade_count = cls._parse_num(num_objs[0].text)
        free_user_count =  cls._parse_num(num_objs[1].text)
        pay_user_count =  cls._parse_num(num_objs[2].text)
        isv_url = soup.find(attrs={"class":"entity ui-radius"}).findAll("li")[0].find("a")["href"]
        isv_id =cls._parse_isv_id(isv_url) 
        a_list = soup.find(attrs={"class":"crumb"}).findAll("a")
        cat_id = cls._parse_param("tab_cat_id",a_list[-1]["href"])
        data ={"isv_id":isv_id,"grade_count":grade_count,"free_user_count":free_user_count,"pay_user_count":pay_user_count,"score":score,"cat_id":cat_id}
        return data

    @classmethod
    def parse_isv_article(cls,html):
        """解析isv页面中的article列表"""
        if not html or "tpListTable" not in html:
            logger.info("parse_isv_article not found tpListTable")
            return None
        if type(html) == type(""):
            html = html.encode("utf-8")
        soup = BeautifulSoup(html)
        tr_list = soup.find(attrs={"class":"tpListTable"}).find("tbody").findAll("tr")
        article_list = []
        article_base_list = []
        for obj in tr_list:
             tds = obj.findAll("td")
             service_code_url = tds[0].find("a")["href"]
             service_code = cls._parse_service_code(service_code_url)
             pic = tds[0].find("img")["src"]
             name = tds[1].find("dt").find("a").text
             desc = tds[1].find(attrs={"class":"desc"}).text
             user_count = tds[3].text
             pv = tds[4].text
             article = {"name":name,"article_code":service_code,"pic":pic,"desc":desc}
             article_base = {"article_code":service_code,"user_count":user_count,"pv":pv}
             article_list.append(article)
             article_base_list.append(article_base)
        return {"article_list":article_list,"article_base_list":article_base_list} 


    @classmethod
    def parse_orders(cls,html):
        if type(html) == type(""):
            html = html.encode("utf-8")
        data_list = html.split('\n')
        if len(data_list) ==2:
            currentPage = 'currentPage'
            pageCount = 'pageCount'
            rateNum = 'rateNum'
            rateSum = 'rateSum'
            isB2CSeller = 'isB2CSeller'
            nick = 'nick'
            deadline = 'deadline'
            version = 'version'
            isPlanSubed = 'isPlanSubed'
            payTime = 'payTime'
            data = 'data'
            isTryoutSubed = 'isTryoutSubed'
            planUrl = 'planUrl'

            data = eval(data_list[1])
            order_list = []
            for order in data["data"]:
                order["seller_level"] = cls._parse_level(order["rateSum"])
                order["buyer_level"] = cls._parse_level(order["rateNum"])
                order["payTime"] = datetime.strptime(order["payTime"],"%Y-%m-%d %H:%M:%S")
                if order["nick"].find('<font title="') != -1:
                    order["nick"] =  order["nick"].split('"')[1]
            return data 
    
    @classmethod
    def parse_suggests(cls,html):
        if type(html) == type(""):
            html = html.encode("utf-8")
        data_list = html.split('\n')
        true = True
        false= False 
        null = None
        if len(data_list) >2:
            info = data_list[1][19:-2]
            data = eval(info)
            if data and data["success"]:
                for suggest in data["comments"]:
                    suggest["suggestion"] = cls._parser.unescape(suggest["suggestion"])
                    suggest["gmtCreate"] = cls._parse_time(suggest["gmtCreate"])
                    suggest["gmtModified"] = cls._parse_time(suggest["gmtModified"])
                    suggest["scoreDate"] = cls._parse_time(suggest["scoreDate"])
                    level_text_group = re.search(r"(\d+)_(\d+)",suggest["userLevelPic"])
                    level = 0
                    if level_text_group:
                        level = cls._parse_level(level_text_group.group(0))
                    suggest["level"] = level
                return data 



    @classmethod
    def parse_isv_id(cls,html):
        """获取isv首页的page_id"""
        if not html or "page_id" not in html:
            logger.info("parse_isv_id not fond page_id")
            return
        soup = BeautifulSoup(html)
        page_url = soup.find(attrs={"class":"nav-entity"}).findAll("li")[1].find("a")["href"]
        page_id = re.findall(r"page_id=([^&]+)",page_url)[0]
        return page_id

    @classmethod
    def _parse_num(cls,num_text):
        """去除文字中的汉字,并千万转化为数字"""
        filter_words =(u"次/30天",u"次",u"人",",")
        new_text = num_text
        for x in filter_words:new_text = new_text.replace(x,"")
        if u"少于" in new_text:
            return new_text
        if u"万" in  new_text:
            return float(new_text.replace(u"万",""))*10000
        return float(new_text)

    @classmethod
    def _parse_isv_id(cls,isv_url):
        """从url中解析isv_id"""
        isv_id = re.findall(r"isv_id=([^&]+)",isv_url)[0]
        return isv_id

    @classmethod
    def _parse_service_code(cls,service_code_url): 
        """从url中解析service_code"""
        service_code = re.findall(r"service_code=([^&]+)",service_code_url)[0]
        return service_code

    @classmethod
    def _parse_param(cls,key,url):
        """从url中解析isv_id"""
        v = re.findall(key+"=([^&]+)",url)[0]
        return v

    @classmethod
    def _parse_level(cls,level_text):
        """等级转化为数字"""
        if not level_text:
            return 0
        num_list = level_text.split("_")
        return (int(num_list[0])-1)*5  + int(num_list[1])

    @classmethod
    def _parse_time(cls,millisecond):
        """毫秒数转化为时间"""
        return datetime.utcfromtimestamp(millisecond/1000)

