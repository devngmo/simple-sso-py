import json
from sp_collection_storage import CollectionStorageProvider 

class OauthClientStorageService():
    def __init__(self, storageProvider: CollectionStorageProvider):
        self.storageProvider = storageProvider

    def add(self, clientID, clientSecret):
        print('Oauth Client Storage: add %s - %s' % (clientID, clientSecret))
        return self.storageProvider.addDocument('oauth_clients', clientID, { 'client_id': clientID, 'client_secret': clientSecret })

    def find(self, clientID, clientSecret):
        return self.storageProvider.findOne('oauth_clients', {'client_id': clientID, 'client_secret' : clientSecret})

    def findByID(self, clientID):
        return self.storageProvider.findOne('oauth_clients', {'_id': clientID })

    def getAll(self):
        return self.storageProvider.getAll('oauth_clients')