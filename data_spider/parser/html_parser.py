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

import re
import urllib
import simplejson as json
from HTMLParser import HTMLParser 
from BeautifulSoup import BeautifulSoup

class HtmlParser(object):

    @classmethod
    def parse_article(cls,html):
        """article解析"""
        if not html or "J_Service" not in html:
            return None
        if type(html) == type(""):
            #html = html.encode("utf-8")
            pass
        soup = BeautifulSoup(html)
        container = soup.find(attrs ={"id":"J_Service"})
        cat_id = soup.find(attrs={"id":"content"})["data-spm"]
        article_obj_list = container.findAll("tr")
        parser = HTMLParser()
        article_list =[]
        isv_list = []
        for article_obj in article_obj_list:
            d1 = article_obj.find(attrs = {"class":"item-meta"})
            pic = d1.find("img")["src"]
            service_code = re.findall(r"service_code=(.+)&trace\w+",d1.find("a")["href"])[0]
            name = d1.find("h4").find("a")["title"]
            desc = parser.unescape(d1.find("p",{"class":"desc"}).text)
            d2 = d1.find(attrs = {"class":"concat"}).find("a")
            isv_name = parser.unescape(d2.text)
            isv_id = re.findall(r"isv_id=(\d+)",d2["href"])[0]

            score = article_obj.find("span",{"class":"ui-no-rate"})["title"]
            user_count = article_obj.findAll("td")[2].text
            price = article_obj.findAll("td")[3].find("p").text

            article = {"article_code":service_code,"pic":pic,"name":name,"isv_id":isv_id,"desc":desc,"cat_id":cat_id}
            isv = {"isv_id":isv_id,"name":isv_name}
            article_list.append(article)
            isv_list.append(isv)
        return {"isv_list":isv_list,"article_list":article_list}
