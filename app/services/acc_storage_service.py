#from ..models.account import Account
#from ..providers.collection_storage_provider import CollectionStorageProvider

class AccountStorageService():
    def __init__(self, storageProvider):
        self.storageProvider = storageProvider

    def addAccount(self, account):
        return self.storageProvider.addDocument('accounts', account.id, account)

    def updateAccount(self, account):
        return self.storageProvider.updateDocument('accounts', account.id, account)

    def findOne(self, query):
        return self.storageProvider.findOne('accounts', query)