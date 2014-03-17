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
user_conn = Connection(host=MGDBS['user']['HOST'],port=MGDBS['user']['PORT'])


sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))
log_path = os.path.normpath(os.path.join(os.path.dirname(__file__),'../user_center.log'))

from user_center.conf import set_env
set_env.getEnvReady()
logger = logging.getLogger("user_center")
hdlr = logging.FileHandler(log_path)
hdlr.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s:%(lineno)-15d %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
logger.propagate = False


#id 保证唯一 可以不连续
WORKER_DICT = {
        1:'雯雯',
        2:'牛牛',
        3:'贝贝',
        4:'欣欣',
        5:'龙龙',
        6:'蓉蓉',
        7:'轩轩',
        8:'西西',
        9:'珍珍',
        121:'嘉嘉',
        11:'茂茂',
        }
FULL_NUM = 5000

ARTICLE_LIST = ['ts-1796606', 'ts-1797607', 'ts-1817244']
STATUS_ARTICLE_LIST = ['ts-1796606', 'ts-1797607']
WORKER_ID_XUQIAN = [3,4,5,6,12,16,51,52,53,54]
WORKER_ID_VIP = [1,7,8,101]

