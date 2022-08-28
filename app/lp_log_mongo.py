import json
from s_log import LogProviderInterface
import mongo_helper


def asJsonOrText(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        return x
    if isinstance(x, object):
        return json.dumps(x)
    return json.dumps(x)

class LogProviderMongo(LogProviderInterface):
    def __init__(self, credential, dbName):
        self.client = mongo_helper.initClient(credential)
        self.dbName = dbName
        self.db = self.client[dbName]

    def info(self, tag, msg):
        self.db.logs.insert_one({'v': 'i', 'tag': tag, 'msg': asJsonOrText(msg)})

    def debug(self, tag, msg, state=None):
        if state != None:
            self.db.logs.insert_one({'v': 'd', 'tag': tag, 'msg': asJsonOrText(msg), 'state': state})
        else:
            self.db.logs.insert_one({'v': 'd', 'tag': tag, 'msg': asJsonOrText(msg)})

    def error(self, tag, msg):
        self.db.logs.insert_one({'v': 'e', 'tag': tag, 'msg': asJsonOrText(msg)})

    def fatal(self, tag, msg):
        self.db.logs.insert_one({'v': 'fe', 'tag': tag, 'msg': asJsonOrText(msg)})