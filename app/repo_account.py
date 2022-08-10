from munch import Munch
from s_acc_storage import AccountStorageService
import utils, defs
from models import account as ModelAccount

class AccountRepository():
    def __init__(self, storageService: AccountStorageService):
        self.storateService = storageService
    
    def registerNewAccount(self, account:ModelAccount.Account):
        print('AccountRepo: registerNewAccount...')
        
        if utils.isValidEmailAddress(account.id):
            acc = self.findByMail(account.id, account.passhash)
            if acc != None:
                return Munch({ 'errCode':defs.ERRCODE_REGISTER_EMAIL_ALREADY_EXIST })
        else:
            acc = self.findByPhone(account.id, account.passhash)
            if acc != None:
                return Munch({ 'errCode':defs.ERRCODE_REGISTER_PHONE_ALREADY_EXIST })
        
        self.storateService.addAccount(account)
        return Munch({ 'errCode': defs.ERRCODE_NONE })

    def updateAccount(self, account):
        self.storateService.updateAccount(account)

    def findByMail(self, email, passhash):
        return self.storateService.findOne({'email': email, 'passhash': passhash})

    def findByPhone(self, phone, passhash):
        return self.storateService.findOne({'phone': phone, 'passhash': passhash})
    
    def finByID(self, id):
        print('Account Repository: find by ID: %s' % id)
        return self.storateService.findOne({'_id' : id})