import json
from sp_collection_storage import CollectionStorageProvider 
from models import account as ModelAccount

class AccountStorageService():
    def __init__(self, storageProvider: CollectionStorageProvider):
        self.storageProvider = storageProvider

    def addAccount(self, client_id, account: ModelAccount.Account):
        print('Account Storage: add account: %s' % account.id)
        return self.storageProvider.addDocument('accounts_%s' % client_id, account.id, account.__dict__)

    def updateAccount(self, client_id, account):
        return self.storageProvider.updateDocument('accounts_%s' % client_id, account['id'], account)

    def findOne(self, client_id, query):
        print('findOne:')
        print(query)
        print('Account Storage Service: find one: %s' % json.dumps(query))
        return self.storageProvider.findOne('accounts_%s' % client_id, query)

    def getAll(self, client_id):
        return self.storageProvider.getAll('accounts_%s' % client_id)