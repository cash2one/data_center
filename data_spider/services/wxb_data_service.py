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

from data_spider.conf.settings import WXB_ACCOUNT,RPT_PATH
from data_spider.tool.wxb_tools import login,download_rpt_strong
from data_spider.tool.xls_tools import excel_table_byindex,excel_table_from_file_byindex
from data_spider.db_models.adgroup_wxb import AdgroupWXB
from data_spider.db_models.tag_wxb import TagWXB
from data_spider.db_models.campaign_wxb import CampaignWXB
logger = logging.getLogger(__name__)

class WxbDataService(object):
    """网销宝数据"""

    @classmethod
    def sync_wxb(cls,rpt_date,sync_campaign = False,sync_adgroup = False,sync_tag = False):
        """
        网销宝计划报表同步,
        sync_campaign :是否同步计划报表
        sync_adgroup:是否同步推广页报表
        sync_tag :是否同步定向报表
        """
        start_date = datetime.combine(rpt_date,dt.time())
        end_date = start_date
        result = login(WXB_ACCOUNT["nick"],WXB_ACCOUNT["passwd"],WXB_ACCOUNT["_tb_token"],WXB_ACCOUNT["agent_nick"])
        if not result:
            logger.info("sync_campaigns_wxb login failed")
            return  
        token = result["token"]
        if sync_campaign:
            campaign_rpt = download_rpt_strong(start_date, end_date, token, 'campaign', RPT_PATH)
            if campaign_rpt:
                colnames = ["campaign","pv","click","cost","cpc","ctr"]
                data_list = excel_table_byindex(campaign_rpt,colnames=colnames)
                for data in data_list:
                    data["rpt_date"] = datetime.combine(rpt_date,dt.time())
                CampaignWXB.upsert_campaign_wxb_list(data_list)

        if sync_adgroup: 
            page_rpt = download_rpt_strong(start_date, end_date, token, 'adgroup', RPT_PATH)
            colnames = ["page","campaign","pv","click","cost","cpc","ctr"]
            data_list = excel_table_byindex(page_rpt,colnames=colnames)
            if data_list:
                for data in data_list:
                    data["rpt_date"] = datetime.combine(rpt_date,dt.time())
                AdgroupWXB.upsert_adgroup_wxb_list(data_list)
        if sync_tag:
            keyword_rpt = download_rpt_strong(start_date, end_date, token, 'tag', RPT_PATH)
            if keyword_rpt:
                colnames = ["position", "pic", "plan" , "pv", "click", "cost","cpc","ctr"]
                data_list = excel_table_byindex(keyword_rpt,colnames=colnames)
                for data in data_list:
                    data["rpt_date"] = datetime.combine(rpt_date,dt.time())
                TagWXB.upsert_tag_wxb_list(data_list)

if __name__ == "__main__":
    article_code = "ts-1796606"
    article_code = "appstore-9092"
    start_date = datetime(2014,3,19)
    end_date = datetime(2014,3,19)
    WxbDataService.sync_wxb(start_date,sync_campaign = True,sync_adgroup=True,sync_tag = True)
