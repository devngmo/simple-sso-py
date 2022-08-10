import uuid
from sp_collection_storage import CollectionStorageProvider

class TokenStorageService():
    def __init__(self, storageProvider:CollectionStorageProvider):
        self.storageProvider = storageProvider

    def addToken(self, token, metadata):
        return self.storageProvider.addDocument('tokens', token, metadata)

    def get(self, token):
        return self.storageProvider.findOne('tokens', {'_id': token})