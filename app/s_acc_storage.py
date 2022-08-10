import json
from sp_collection_storage import CollectionStorageProvider 
from models import account as ModelAccount

class AccountStorageService():
    def __init__(self, storageProvider: CollectionStorageProvider):
        self.storageProvider = storageProvider

    def addAccount(self, account: ModelAccount.Account):
        print('Account Storage: add account: %s' % account.id)
        return self.storageProvider.addDocument('accounts', account.id, account.__dict__)

    def updateAccount(self, account):
        return self.storageProvider.updateDocument('accounts', account['id'], account)

    def findOne(self, query):
        print('findOne:')
        print(query)
        print('Account Storage Service: find one: %s' % json.dumps(query))
        return self.storageProvider.findOne('accounts', query)