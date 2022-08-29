from datetime import datetime
import json, utils
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