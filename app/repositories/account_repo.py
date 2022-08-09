from munch import Munch
#from .. import defs
#from ..models.account import Account
#from ..services.acc_storage_service import AccountStorageService
#from .. import utils

class AccountRepository():
    def __init__(self, storageService):
        self.storateService = storageService
    
    def registerNewAccount(self, account):
        print(__package__)
        from .. import utils, defs
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
        return self.storateService.findOne({'_id', id})