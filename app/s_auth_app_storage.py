import json
from models.auth_app import AuthApplicationRegistrationModel, AuthApplication
class AuthAppStorageProviderInterface():
    def add(self, appInfo: AuthApplication):
        return None

    def getByAppID(self, appID):
        return None

    def getByAppCode(self, appCode):
        return None

    def getAll(self):
        return []

    def deleteAll(self):
        return []
class AuthAppStorageService():
    def __init__(self, storageProvider: AuthAppStorageProviderInterface):
        self.storageProvider = storageProvider

    def add(self, appInfo: AuthApplication):
        return self.storageProvider.add(appInfo)

    def getByAppCode(self, appCode):
        return self.storageProvider.getByAppCode(appCode)

    def getByAppID(self, appID):
        return self.storageProvider.getByAppID(appID)

    def getAll(self):
        return self.storageProvider.getAll()
    
    def deleteAll(self):
        return self.storageProvider.deleteAll()