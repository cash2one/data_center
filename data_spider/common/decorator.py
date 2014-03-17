#encoding=utf8
"""doc string for module"""
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import logging
import traceback
import inspect

from time import  sleep
from datetime import datetime
from django.http import HttpResponseBadRequest
import simplejson as json
from validictory import  ValidationError
from validictory import  validate
from pymongo.errors import AutoReconnect, OperationFailure, PyMongoError

from TaobaoSdk.Exceptions import ErrorResponseException

from db_exceptions.exceptions import  MongodbException

logger = logging.getLogger(__name__)




def mongo_exception(func):
    """
    decorator to catch and deal with mongodb exception in a uniform way.

    example:
    if AutoReconnect exception occurs, we will catch it and retry the last mongodb operation.

    NOTICE:
    this  decorator can be only used for **transaction**, if not, data maybe in a mess.

    """

    def wrapped_func(*args, **kwargs):
        retry_times = 0
        while True:
            try:
                return func(*args, **kwargs)
            except AutoReconnect, e:
                retry_times+=1
                if retry_times > 5:
                    logging.exception("got an exception when operate on mongodb")
                    raise MongodbException(msg=('shop_mongo_exception:%s'%str(e)))
                sleep(2)

            except  OperationFailure, e:
                logging.exception("got an exception when operate on mongodb")
                raise MongodbException(msg=('shop_mongo_exception:%s'%str(e)))

            except PyMongoError,e:
                logging.exception("got an exception when operate on mongodb")
                raise MongodbException(msg=('shop_mongo_exception:%s'%str(e)))
    return wrapped_func

def operate_exception(MAX_RETRY_TIMES=3):
    def _wrapper_func(func):
        def _wraped_func(*args,**kwargs):
            retry_time=0
            res=None
            next=True
            while next:
                retry_time+=1
                if retry_time>MAX_RETRY_TIMES:
                    break
                try:
                    res=func(*args,**kwargs)
                    next=False
                except socket.timeout:
                    retry_time+=1
                    logger.error("socket timeout")
                except Exception,e:
                    retry_time+=1
                    logger.exception("got an unknow exception")
            return res
        return _wraped_func
    return _wrapper_func
