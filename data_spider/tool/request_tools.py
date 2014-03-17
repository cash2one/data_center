#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-03-14 15:33
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import urllib2
import urllib
from data_spider.common.decorator import operate_exception

@operate_exception()
def get_response(url,params = None):
    if not params:
        conn = urllib2.urlopen(url)
    else:
        post_data = urllib.urlencode(params)
        req = urllib2.Request(url, post_data)
        conn = urllib2.urlopen(req)
    html = conn.read()
    return html

