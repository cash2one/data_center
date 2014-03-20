#encoding=utf8
# Django settings for xuanciw project.
import os, sys
import pymongo
from pymongo import Connection
import logging

if pymongo.version.startswith("2.5"):
    import bson.objectid
    import bson.json_util
    pymongo.objectid = bson.objectid
    pymongo.json_util = bson.json_util
    sys.modules['pymongo.objectid'] = bson.objectid
    sys.modules['pymongo.json_util'] = bson.json_util



#MONGODB SETTINGS
MGDBS = {
        'user':{
            'HOST':'app.maimiaotech.com',
            'PORT':2201,
            'USER':'',
            'PASSWORD':''
        }
    }


#利用mongodb 自带的connection poll 来管理数据库连接
mongoConn = Connection(host=MGDBS['user']['HOST'],port=MGDBS['user']['PORT'])


sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))
log_path = os.path.normpath(os.path.join(os.path.dirname(__file__),'../data_spider.dev.log'))

from data_spider.conf import set_env
set_env.getEnvReady()
logger = logging.getLogger("data_spider")
hdlr = logging.FileHandler(log_path)
hdlr.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s:%(lineno)-15d %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
logger.propagate = False

#网销宝账号
WXB_ACCOUNT = {"nick":"麦苗科技营销","passwd":"Mm-marketing2#","_tb_token":"ylD7uO2T8sm","agent_nick":None}
base_path = os.path.join(os.path.dirname(__file__),'../')
RPT_PATH =  os.path.normpath(os.path.join(base_path,"rpt"))
