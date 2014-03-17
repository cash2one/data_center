#encoding=utf8
__author__ = 'xieguanfu@maimiaotech.com'


import sys
import os
import logging
import logging.config
from datetime import  datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
    logging.config.fileConfig('../conf/log4p_file_console.conf')

from user_center.conf import settings 
from user_center.common.decorator import mongo_exception

class App(object):
    """
    class to operate app collections
    """

    _conn = settings.user_conn
    coll = _conn['user_center']['app']

    @classmethod
    @mongo_exception
    def upsert_app(cls,app_dict):
        filter = {'_id':app_dict['app_id']}
        if "_id" in app_dict:
            app_dict.pop("_id")
        cls.coll.update(filter, {"$set":app_dict}, upsert=True,j=True)
        


    @classmethod
    @mongo_exception
    def get_app_by_app_id(cls,app_id):
        filter={"_id":app_id}
        return cls.coll.find_one(filter)
