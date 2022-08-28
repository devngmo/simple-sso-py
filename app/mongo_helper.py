from datetime import datetime
import json, utils
from pymongo import MongoClient
from s_acc_storage import AccountStorageProviderInterface
from urllib.parse import quote

def createConnectionString(credential):
    host = utils.getProperty(credential,'host')
    port = utils.getProperty(credential,'port')
    user = utils.getProperty(credential,'user')
    passwd = utils.getProperty(credential,'passwd')
    pwdEncoded = quote(passwd)
    acc = '{user}:{passwd}'.format(user=user, passwd=pwdEncoded)
    extra = ''
    if len(acc) > 1 and user != None and passwd != None:
        acc = acc + '@'
        extra = '/?authMechanism=DEFAULT'
    return 'mongodb://{acc}{host}:{port}{extra}'.format(acc=acc, host=host, port=port, extra=extra)

def initClient(credential):
    if isinstance(credential, str):
        connectionStr = credential
    else:
        connectionStr = createConnectionString(credential)
    print('init MongoClient: ', connectionStr)
    client = MongoClient(connectionStr)
    return client
