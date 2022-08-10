import uuid

from s_token_storage import TokenStorageService

class TokenRepository():
    def __init__(self, tokenStorage: TokenStorageService):
        self.tokenStorage = tokenStorage

    def add(self, token, metadata):
        self.tokenStorage.addToken(token, metadata)

    def get(self, token):
        return self.tokenStorage.get(token)

    def createToken(self, metadata):
        token = uuid.uuid4().hex
        self.add(token, metadata)
        return token

    def addClientToken(self, client_id, token, metadata):
        self.tokenStorage.addClientToken(client_id, token, metadata)

    def getClientToken(self, client_id, token):
        return self.tokenStorage.getClientToken(client_id, token)

    def createClientToken(self, client_id, metadata):
        token = uuid.uuid4().hex
        self.addClientToken(client_id, token, metadata)
        return token

    