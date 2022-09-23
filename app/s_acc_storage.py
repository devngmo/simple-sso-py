import json
from sp_collection_storage import CollectionStorageProvider 
from models import account as ModelAccount

class AccountStorageProviderInterface():
    def addAccount(self, account: ModelAccount.Account):
        return None

    def replaceUnactivatedAccount(self, account_id, account):
        return None

    def updateAccount(self, account_id, changes):
        return None

    def getAccountByID(self, account_id):
        return None

    def getAllAccounts(self):
        return None

    def getAllTenantAccounts(self):
        return None

    def deleteAllAccounts(self):
        return None

    def findByMail(self, email):
        return None

    def findByPhone(self, phone):
        return None

    def saveUserDeviceInfo(self, account_id:str, fcm_token:str, apn_token:str, device_info:str, installation_id:str):
        return None

class AccountStorageService():
    def __init__(self, storageProvider: AccountStorageProviderInterface):
        self.storageProvider = storageProvider

    def replaceUnactivatedAccount(self, account_id, account):
        return self.storageProvider.replaceUnactivatedAccount(account_id, account)

    def addAccount(self, account: ModelAccount.Account):
        return self.storageProvider.addAccount(account)

    def updateAccount(self, account_id, changes):
        return self.storageProvider.updateAccount(account_id, changes)

    def getAccountByID(self, account_id):
        return self.storageProvider.getAccountByID(account_id)

    def getAllAccounts(self):
        return self.storageProvider.getAllAccounts()

    def getAllTenantAccounts(self):
        return self.storageProvider.getAllTenantAccounts()

    def deleteAllAccounts(self):
        return self.storageProvider.deleteAllAccounts()

    def findByMail(self, email):
        return self.storageProvider.findByMail(email)

    def findByPhone(self, phone):
        return self.storageProvider.findByPhone(phone)

    def saveUserDeviceInfo(self, account_id:str, fcm_token:str, apn_token:str, device_info:str, installation_id:str):
        return self.storageProvider.saveUserDeviceInfo(account_id, fcm_token, apn_token, device_info, installation_id)