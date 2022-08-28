from datetime import datetime
import json, utils
from pymongo import MongoClient
from s_acc_storage import AccountStorageProviderInterface
from urllib.parse import quote
import redis

def createPoolFromModel(credential):
    host = utils.getProperty(credential,'host')
    port = utils.getProperty(credential,'port')
    passwd = utils.getProperty(credential,'passwd')
    if passwd != None and len(passwd) > 0:
        return redis.ConnectionPool(host=host, port=port, password=passwd)

    return redis.ConnectionPool(host=host, port=port)
    
def createPoolFromString(credential):
    return redis.ConnectionPool(credential)

def initClient(credential):
    if isinstance(credential, str):
        pool = createPoolFromString(credential)
        return redis.Redis(connection_pool=pool)
    else:
        pool = createPoolFromModel(credential)
        return redis.Redis(connection_pool=pool)
