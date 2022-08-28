from ctypes import util
from munch import Munch
from s_acc_storage import AccountStorageService
import utils, defs
from models import account as ModelAccount

class AccountRepository():
    def __init__(self, storageService: AccountStorageService):
        self.storateService = storageService
    
    def registerNewAccount(self, account:ModelAccount.Account):
        print('AccountRepo: registerNewAccount...')
        
        acc = self.storateService.findByMail(account.email)

        if acc != None:
            if acc['activated'] == True:
                return Munch({ 'errCode':defs.ERRCODE_REGISTER_PHONE_ALREADY_EXIST })
            else:
                self.storateService.replaceUnactivatedAccount(acc['_id'], account)
        else:
            acc = self.storateService.addAccount(account)

        return Munch({ 'errCode': defs.ERRCODE_NONE, 'account': acc })

    def updateAccount(self, account_id, changes):
        return self.storateService.updateAccount(account_id, changes)

    def finByID(self, account_id):
        print('Account Repository: find by ID: %s' % account_id)
        return self.storateService.getAccountByID(account_id)

    def getAll(self):
        return self.storateService.getAllAccounts()

    def getAllTenants(self):
        return self.storateService.getAllTenantAccounts()

    def deleteAll(self):
        return self.storateService.deleteAllAccounts()

    def findByEmail(self, email):
        return self.storateService.findByMail(email)

    def findByPhone(self, phone):
        return self.storateService.findByPhone(phone)

    def upgradeToTenant(self, account_id):
        return self.storateService.updateAccount(account_id, {'is_tenant': True})