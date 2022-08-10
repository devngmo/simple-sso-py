import datetime, utils
from http.client import HTTPException
from pydantic import BaseModel
from models import account as ModelAccount
from repo_token import TokenRepository
from repo_account import AccountRepository

class LoginModel(BaseModel):
    emailOrPhone: str
    password: str

class SignInService():
    def __init__(self, accountRepo: AccountRepository, tokenRepo: TokenRepository):
        self.accountRepo = accountRepo
        self.tokenRepo = tokenRepo

    def signIn(self, client_id, loginModel):
        passhash = ModelAccount.createPasshash(loginModel.password)
        
        acc = None
        if utils.isValidEmailAddress(loginModel.emailOrPhone):
            acc = self.accountRepo.findByMail(client_id, loginModel.emailOrPhone, passhash)
        else:
            acc = self.accountRepo.findByPhone(client_id, loginModel.emailOrPhone, passhash)
        if acc == None:
            raise HTTPException(status_code=404, detail="Invalid account")

        elif acc['activated'] == False:
            raise HTTPException(status_code=403, detail="you can not login with inactivated account")

        publicInfo = acc
        del publicInfo['passhash']
        del publicInfo['activated']

        loginSession = {'client_id': client_id, 'info': publicInfo, 'ttl': 60*60, 'expire': datetime.datetime.now() + datetime.timedelta(hours=1) }
        token = self.tokenRepo.createClientToken(client_id, loginSession )
        return { 'access_token': token }
