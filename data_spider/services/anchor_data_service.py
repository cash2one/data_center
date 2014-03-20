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

from data_spider.parser.log_parser import LogParser
from data_spider.db_models.anchor import Anchor
logger = logging.getLogger(__name__)

class AnchorDataService(object):


    @classmethod
    def sync_anchor_by_file(cls,file_path):
        """ 日志文件中读取访问日志"""
        try:
            f = open(file_path,'r')
            anchor_list = []
            for line in f:
                anchor = LogParser.parse_anchor_log(line)
                if anchor:
                    anchor_list.append(anchor)
            Anchor.upsert_anchor_list(anchor_list)
        except Exception,e:
            print e
            logger.exception("sync anchor from file:%s" %(file_path))

    @classmethod
    def sync_anchor_by_log(cls,log):
        if not log:
            return
        lines = log.split("\n")
        anchor_list = []
        for line in lines:
            anchor = LogParser.parse_anchor_log(line)
            if anchor:
                anchor_list.append(anchor)
        Anchor.upsert_anchor_list(anchor_list)

    
if __name__ == "__main__":
    article_code = "ts-1796606"
    article_code = "appstore-9092"
    path = "/home/xiegf/aa.log"
    AnchorDataService.sync_anchor_by_file(path)
