import datetime, utils, json
from s_log import LogService

from pydantic import BaseModel
from models import account as ModelAccount
from repo_token import TokenRepository
from repo_account import AccountRepository
from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256

import defs
class LoginModel(BaseModel):
    emailOrPhone: str
    password: str

    def toJson(self):
        return { 'emailOrPhone' : self.emailOrPhone, 'password': self.password }
class SignInService():
    def __init__(self, logger: LogService, accountRepo: AccountRepository, tokenRepo: TokenRepository):
        self.accountRepo = accountRepo
        self.tokenRepo = tokenRepo
        self.logger = logger

    def signIn(self, app_code, emailOrPhone, password):
        acc = None
        if utils.isValidEmailAddress(emailOrPhone):
            acc = self.accountRepo.findByEmail(emailOrPhone)
        else:
            acc = self.accountRepo.findByPhone(emailOrPhone)


        if acc == None:
            self.logger.debug('SignInService', { 'action': 'signIn', 'app_code': app_code, 'loginModel': {'emailOrPhone': emailOrPhone, 'password' : password}, 'msg': 'account not found by email / phone' }, state='failed')
            raise HTTPException(status_code=404, detail="Invalid username/password")
        elif pbkdf2_sha256.verify(password, acc['passhash']) == False:
            self.logger.debug('SignInService', { 'action': 'signIn', 'app_code': app_code, 'loginModel': {'emailOrPhone': emailOrPhone, 'password' : password}, 'msg': 'passhash not match' }, state='failed')
            raise HTTPException(status_code=401, detail="Invalid username/password")
        elif acc['activated'] == False:
            self.logger.debug('SignInService', { 'action': 'signIn', 'app_code': app_code, 'loginModel': {'emailOrPhone': emailOrPhone, 'password' : password}, 'msg': 'account unactivated' }, state='failed')
            raise HTTPException(status_code=403, detail="you can not login with inactivated account")

        expireTime = datetime.datetime.now() + datetime.timedelta(hours=1)

        accountID = str(acc['_id'])
        tenant_id = acc['parent_tenant_id']
        roles = ['viewer']
        if acc['is_tenant']:
            tenant_id = accountID
            roles = ['admin']

        loginSession = {'id': accountID, 'roles': roles, 'name': acc['name'], 'email': acc['email'], 'is_tenant': acc['is_tenant'], 'tenant_id': tenant_id, 'ttl': 60*60, 'expire': expireTime.isoformat(), 'type': defs.TOKEN_TYPE_AUTH_ACCESS }
        token = self.tokenRepo.createJWTToken( loginSession )
        self.logger.debug('SignInService', { 'action': 'signIn', 'app_code': app_code, 'loginModel': {'emailOrPhone': emailOrPhone, 'password' : password}, 'msg': 'logged in', 'access_token': token }, state='success')

        return { 'access_token': token, 'ttl': 60*60, 'expire': expireTime.isoformat() }
