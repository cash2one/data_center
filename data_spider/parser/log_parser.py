#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-03-19 14:20
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import logging
import re
import urllib
import simplejson as json
from datetime import datetime
logger = logging.getLogger(__name__)

class LogParser(object):

    @classmethod
    def parse_anchor_log(cls,line,ignore_ip = '122.224.126.18'):
        """解析锚点日志,详情页中或北斗等首页中a.gif"""
        DEST_RE = '(\d+\.\d+\.\d+\.\d+)[\s\S]+\[(.+)\]\s+"GET \/a\.gif(\?(\S+),(\d+))?\s+HTTP[\s\S]+"[^"]+"http:\/\/([\w\.]+)\.maimiaotech\.com\/[\s\S]*?user=([\d\.]+)[;|"][\s\S]*' 
        SRC_RE = '(\d+\.\d+\.\d+\.\d+)[\s\S]+\[(.+)\]\s+"GET \/a\.gif[^"]*"[^"]*"(http:.+)"\s+"[\s\S]+" "-" "user=([\d\.]+)[;|"][\s\S]*'

        src_list = []
        dest_users = set()
        if line.find('a.gif') < 0:
            return
        if ignore_ip and ignore_ip in line:
            return 
        m = re.search(SRC_RE, line)
        if m:
            ip = m.group(1)
            gmt_date = datetime.strptime(m.group(2),'%d/%b/%Y:%H:%M:%S +0800')
            source = cls._parse_source_from_refer(m.group(3))
            uid = m.group(4)

            log ={"ip":ip,"rpt_date":gmt_date,"source":source,"uid":uid,"type":0}
            return log
        else:
            m = re.search(DEST_RE, line)
            if m:
                ip = m.group(1)
                gmt_date = datetime.strptime(m.group(2),'%d/%b/%Y:%H:%M:%S +0800')
                nick = m.group(4)
                sid = m.group(5)
                app = m.group(6)
                uid = m.group(7)
                nick = urllib.unquote_plus(nick).decode("string_escape").encode("utf-8")
                log ={"ip":ip,"rpt_date":gmt_date,"nick":nick,"sid":sid,"app":app,"uid":uid,"type":1}
                return log

    @classmethod
    def _parse_source_from_refer(cls,refer_url):
        """获取refer中具体的来源"""
        FROM_RE = '(?:tracelog|from)=([\w-]+)[^&]'
        m = re.search(FROM_RE,refer_url)
        if m:
            return m.group(1)


