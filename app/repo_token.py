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