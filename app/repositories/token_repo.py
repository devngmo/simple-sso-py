import uuid
# from ..providers.collection_storage_provider import CollectionStorageProvider

class TokenRepository():
    def __init__(self, tokenStorage):
        self.tokenStorage = tokenStorage

    def add(self, token, metadata):
        self.tokenStorage.addDocument('tokens', token, metadata)

    def get(self, token):
        return self.tokenStorage.findOne({'_id': token})

    def createToken(self, metadata):
        token = uuid.uuid4().hex
        self.add(token, metadata)
        return token