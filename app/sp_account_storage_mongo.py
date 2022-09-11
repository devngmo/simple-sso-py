from datetime import datetime
import json, utils, hashlib
from turtle import update
from pymongo import MongoClient
from bson.objectid import ObjectId
from urllib.parse import quote

import mongo_helper
from s_acc_storage import AccountStorageProviderInterface
from models import account as ModelAccount

class AccountStorageProviderMongo(AccountStorageProviderInterface):
    def __init__(self, credential, dbName):
        self.dbName = dbName
        self.client = mongo_helper.initClient(credential)
        self.accDB = self.client[dbName]
        self.accounts = self.accDB.accounts
        self.logs = self.accDB.logs

    def _log(self, entry):
        print('AccountStorageProviderMongo: %s' % json.dumps(entry))
        self.logs.insert_one(entry)

    def saveUserDeviceInfo(self, account_id:str, fcm_token:str, apn_token:str, device_info:str):
        try:
            device_info_model = json.loads(device_info)
            acc = self.getAccountByID(account_id)
            devices = []
            if 'devices' in acc:
                devices = acc['devices']

            md5 = hashlib.md5()
            md5.update(device_info.encode('utf-8'))
            device_hash_id = md5.hexdigest() # str(int(md5.hexdigest(), 16))
            print('device_hash_id ', device_hash_id)

            d = None
            for existedDevice in devices:
                if existedDevice['hash_id'] == device_hash_id:
                    d = existedDevice
                    break
            if d == None:
                d = { 'hash_id': device_hash_id, 'info': device_info_model }
                devices += [ d ]

            if fcm_token != None:
                d['fcm_token'] = fcm_token
            if apn_token != None:
                d['apn_token'] = apn_token

            resp = self.accounts.update_one({'_id': ObjectId(account_id)}, { '$set': { 'devices': devices } })
            self._log({'action': 'saveUserDeviceInfo', 'account_id': account_id, 'fcm_token': fcm_token, 'apn_token': apn_token, 'device': device_info_model, 'result': { 'acknowledged': f'{resp.acknowledged}', 'modified_count': f'{resp.modified_count}', 'raw_result': f'{resp.raw_result}' }})

        except Exception as ex:
            self._log({'action': 'saveUserDeviceInfo', 'account_id': account_id, 'fcm_token': fcm_token, 'apn_token': apn_token, 'device': device_info_model, 'result': f'Exception {ex}'})


    def replaceUnactivatedAccount(self, account_id, account: ModelAccount.Account):
        print('Account DB [%s]: replace unactivated account: %s' % (self.dbName, account_id))
        doc = account.toDict()
        resp = self.accounts.replace_one({'_id': ObjectId(account_id), 'activated': False}, doc)
        if resp.matched_count == 1 and resp.modified_count == 1:
            self._log({ 'action': 'replaceUnactivatedAccount', 'at': datetime.now().isoformat(), 'account': doc, 'result': { 'err': None, 'raw_result': resp.raw_result } })
            return True
        else:
            self._log({ 'action': 'replaceUnactivatedAccount', 'at': datetime.now().isoformat(), 'account': doc, 'result': { 'err': 'unexpected', 'acknowledged': resp.acknowledged, 'raw_result': resp.raw_result } })
        return False

    def addAccount(self, account: ModelAccount.Account):
        print('Account DB [%s]: add account by email: %s' % (self.dbName, account.email))
        doc = account.toDict()
        doc['devices'] = []
        resp = self.accounts.insert_one(doc)
        doc['_id'] = str(resp.inserted_id)
        #TODO: remove test code
        self.updateAccount(doc['_id'], {'is_tenant':True, 'parent_tenant_id': doc['_id']})

        print(resp.inserted_id)
        self._log({ 'action': 'add_account', 'at': datetime.now().isoformat(), 'account': doc, 'result': { 'err': None, 'inserted_id': '%s' % resp.inserted_id } })
        return doc

    def updateAccount(self, account_id, changes):
        print('Account DB: [%s] update account: %s' % (self.dbName, account_id))
        resp = self.accounts.update_one({'_id': ObjectId(account_id)}, { '$set': changes })
        if resp.modified_count == 1:
            self._log({ 'action': 'update_account', 'at': datetime.now().isoformat(), 'account_id': account_id, 'result': { 'err': None, 'changes': changes } })
            return True
        else:
            self._log({ 'action': 'update_account', 'at': datetime.now().isoformat(), 'account_id': account_id, 'result': { 'err': None, 'changes': changes, 'raw_result': resp.raw_result, 'modified_count': resp.modified_count, 'matched_count': resp.matched_count } })
        return False

    def getAccountByID(self, account_id):
        return self.accounts.find_one({'_id': ObjectId(account_id)})

    def getAllAccounts(self):
        cursor = self.accounts.find({})
        founds = []
        for acc in cursor:
            acc['_id'] = str(acc['_id'])
            founds = founds + [acc]
        return founds

    def getAllTenantAccounts(self):
        cursor = self.accounts.find({'is_tenant': True})
        founds = []
        for acc in cursor:
            acc['_id'] = str(acc['_id'])
            founds = founds + [acc]
        return founds
    
    def deleteAllAccounts(self):
        resp = self.accounts.delete_many({})
        print(resp.raw_result)
        return { 'deleted_count': resp.deleted_count }

    def findByMail(self, email):
        acc = self.accounts.find_one({'email': email})
        if acc != None:
            acc['_id'] = str(acc['_id'])
        return acc

    def findByPhone(self, phone):
        acc = self.accounts.find_one({'phone': phone})
        if acc != None:
            acc['_id'] = str(acc['_id'])
        return acc