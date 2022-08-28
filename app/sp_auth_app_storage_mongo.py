from ast import Delete
from datetime import datetime
import json, utils
from pymongo import MongoClient
from urllib.parse import quote

import mongo_helper
from models.auth_app import AuthApplication, AuthApplicationRegistrationModel
from s_auth_app_storage import AuthAppStorageProviderInterface
from models import account as ModelAccount
from s_log import LogService
class AuthAppStorageProviderMongo(AuthAppStorageProviderInterface):
    def __init__(self, logger: LogService, credential, dbName):
        self.logger = logger
        self.dbName = dbName
        self.client = mongo_helper.initClient(credential)
        self.db = self.client[dbName]
        self.clients = self.db.clients
        self.logs = self.db.logs

    def add(self, appInfo: AuthApplication):
        resp = self.clients.insert_one(appInfo.toDict())
        self.logger.info('AuthAppStorageProviderMongo', {'action': 'add', 'app': appInfo.toDict(), 'inserted_id': str(resp.inserted_id)})
        return str(resp.inserted_id)

    def getByAppID(self, appID):
        return self.clients.find_one({ '_id': appID })

    def getByAppCode(self, appCode):
        return self.clients.find_one({ 'code': appCode })

    def getAll(self):
        cursor = self.clients.find({})
        ls = []
        for c in cursor:
            ls += [c]
        return ls

    def deleteAll(self):
        resp = self.clients.delete_many({})
        print(resp.raw_result)
        return { 'deleted_count': resp.deleted_count }