import datetime, utils
from pydantic import BaseModel
from models import account as ModelAccount
class LoginModel(BaseModel):
    emailOrPhone: str
    password: str

class AutheticationService():
    def __init__(self, accountRepo, tokenRepo):
        self.accountRepo = accountRepo
        self.tokenRepo = tokenRepo

    def login(self, loginModel):
        passhash = ModelAccount.createPasshash(loginModel.password)
        result = None
        if utils.isValidEmailAddress(loginModel.emailOrPhone):
            result = self.accountRepo.findByMail(loginModel.emailOrPhone, passhash)
        else:
            result = self.accountRepo.findByPhone(loginModel.emailOrPhone, passhash)
        if result == None:
            return { 'errCode': 1, 'msg': 'Invalid account / password' }
        elif result['activated'] == False:
            return { 'errCode': 2, 'msg': 'Account was not activated yet' }

        loginSession = { 'info': result, 'ttl': 60*60, 'expire': datetime.datetime.now() + datetime.timedelta(hours=1) }
        token = self.tokenRepo.createToken( loginSession )
        return { 'errCode': 0, 'token': token }