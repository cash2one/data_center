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

from data_spider.tool.request_tools import get_response
from data_spider.parser.html_parser import HtmlParser

class ZtcDataService(object):

    @classmethod
    def sync_article_by_cat(cls,cat_id):
        """按照类目获取该类目下的isv以及article"""
        url = "http://fuwu.taobao.com/ser/list.htm?tab_cat_id=51052018&current=-1&is_multi_list=0&primary_sort_desc=true&cat_map_id=%s&tracelog=category&current_page=1" % cat_id
        html = get_response(url)
        data = HtmlParser.parse_article(html)

    
if __name__ == "__main__":
    ZtcDataService.sync_article_by_cat(51052018)
