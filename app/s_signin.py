import datetime, utils
from http.client import HTTPException
from pydantic import BaseModel
from models import account as ModelAccount
class LoginModel(BaseModel):
    client_id: str
    emailOrPhone: str
    password: str

class SignInService():
    def __init__(self, accountRepo, tokenRepo):
        self.accountRepo = accountRepo
        self.tokenRepo = tokenRepo

    def signIn(self, client_id, loginModel):
        passhash = ModelAccount.createPasshash(loginModel.password)
        
        acc = None
        if utils.isValidEmailAddress(loginModel.emailOrPhone):
            acc = self.accountRepo.findByMail(loginModel.emailOrPhone, passhash)
        else:
            acc = self.accountRepo.findByPhone(loginModel.emailOrPhone, passhash)
        if acc == None:
            raise HTTPException(status_code=404, detail="Invalid account")

        elif acc['activated'] == False:
            raise HTTPException(status_code=403, detail="you can not login with inactivated account")

        publicInfo = acc
        del publicInfo['passhash']
        del publicInfo['activated']

        loginSession = {'client_id': client_id, 'info': publicInfo, 'ttl': 60*60, 'expire': datetime.datetime.now() + datetime.timedelta(hours=1) }
        token = self.tokenRepo.createToken( loginSession )
        return { 'access_token': token }
