class TokenStorageProviderInterface():
    def __init__(self):
        pass
        
    def addToken(self, token, metadata):
        return None

    def getToken(self, token):
        return None

class TokenStorageService():
    def __init__(self, storageProvider:TokenStorageProviderInterface):
        self.storageProvider = storageProvider

    def addToken(self, token, metadata):
        return self.storageProvider.addToken(token, metadata)

    def getToken(self, token):
        return self.storageProvider.getToken(token)
