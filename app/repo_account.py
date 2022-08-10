from ctypes import util
from munch import Munch
from s_acc_storage import AccountStorageService
import utils, defs
from models import account as ModelAccount

class AccountRepository():
    def __init__(self, storageService: AccountStorageService):
        self.storateService = storageService
    
    def registerNewAccount(self, client_id, account:ModelAccount.Account):
        print('AccountRepo: registerNewAccount...')
        
        if utils.isValidEmailAddress(account.id):
            acc = self.findByMail(client_id, account.id, account.passhash)
            if acc != None:
                return Munch({ 'errCode':defs.ERRCODE_REGISTER_EMAIL_ALREADY_EXIST })
        else:
            acc = self.findByPhone(client_id, account.id, account.passhash)
            if acc != None:
                return Munch({ 'errCode':defs.ERRCODE_REGISTER_PHONE_ALREADY_EXIST })
        
        self.storateService.addAccount(client_id, account)
        return Munch({ 'errCode': defs.ERRCODE_NONE })

    def updateAccount(self, client_id, account):
        self.storateService.updateAccount(client_id, account)

    def findByMail(self, client_id, email, passhash):
        return self.storateService.findOne(client_id, {'email': email, 'passhash': passhash})

    def findByPhone(self, client_id, phone, passhash):
        return self.storateService.findOne(client_id, {'phone': phone, 'passhash': passhash})
    
    def finByID(self, client_id, id):
        print('Account Repository: find by ID: %s' % id)
        return self.storateService.findOne(client_id, {'_id' : id})

    def getAll(self, client_id):
        return self.storateService.getAll(client_id)