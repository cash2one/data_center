'''
Created on 2012-11-17

@author: dk
'''
import os
import sys
import logging
import logging.config

currDir = os.path.normpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(currDir,os.path.pardir))
PROJECT_PAR = os.path.normpath(os.path.join(PROJECT_ROOT,os.path.pardir))


COMM_LIB = os.path.normpath(os.path.join(currDir, '../../../comm_lib/'))
sys.path.append(COMM_LIB)
SDK_LIB=os.path.normpath(os.path.join(currDir,'../../../TaobaoOpenPythonSDK/'))
sys.path.append(SDK_LIB)

def getEnvReady():
    sys.path.insert(0,PROJECT_PAR)
    from tao_models.conf import set_env as tao_models_set_env 
    tao_models_set_env.getEnvReady()

