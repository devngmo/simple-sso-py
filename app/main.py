import base64
import os, sys, json
from typing import Union
from munch import Munch
from fastapi.security import APIKeyHeader

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_DIR)
sys.path.append(os.path.dirname(APP_DIR))
 
from fastapi import FastAPI, Request, Depends, Form, Header, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

import defs, utils
from models import account
from models.auth_app import AuthApplicationRegistrationModel, AuthApplication
from s_oauth2 import Oauth2
from s_signin import LoginModel, SignInService
from s_factory import ServiceFactory
from s_mail import EmailService
from s_token_storage import TokenStorageService
from s_auth_app_storage import AuthAppStorageService
from s_log import LogService
from s_acc_storage import AccountStorageService

from lp_log_mongo import LogProviderMongo
from sp_auth_app_storage_mongo import AuthAppStorageProviderMongo
from sp_account_storage_mongo import AccountStorageProviderMongo
from sp_token_storage_redis import TokenStorageProviderRedis
from sp_in_memory_storage import InMemoryStorageProvider

from repo_account import AccountRepository
from repo_token import TokenRepository
from repo_auth_app import AuthAppRepository

from registration_validator import RegistrationValidator

ALLOW_CREDENTIALS = utils.getEnvBool('ALLOW_CREDENTIALS', False)
ALLOW_ORIGINS = utils.getEnvValue('ALLOW_ORIGINS', '*').split(',')
ALLOW_METHODS = utils.getEnvValue('ALLOW_METHODS', '*').split(',')
ALLOW_HEADERS = utils.getEnvValue('ALLOW_HEADERS', '*').split(',')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ALLOW_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods = ALLOW_METHODS,
    allow_headers = ALLOW_HEADERS
)


ADMIN_APIKEY = utils.getEnvValue('ADMIN_APIKEY', 'admin')
API_ENDPOINT_EMAIL_CONFIRM = utils.getEnvValue('API_ENDPOINT_EMAIL_CONFIRM', None)
GMAIL_ACCOUNT = utils.getEnvValue('GMAIL_ACCOUNT', None)
GMAIL_APP_PASSWORD = utils.getEnvValue('GMAIL_APP_PASSWORD', None)
JWT_SECRET_KEY = utils.getEnvValue('JWT_SECRET_KEY', '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ')
JWT_ALGORITHM = 'RS256' #utils.getEnvValue('JWT_ALGORITHM', 'HS256')

MONGO_HOST = utils.getEnvValue('MONGO_HOST', '')
MONGO_PORT = int(utils.getEnvValue('MONGO_PORT', ''))
MONGO_USER = utils.getEnvValue('MONGO_USER', '')
MONGO_PASS = utils.getEnvValue('MONGO_PASS', '')

REDIS_HOST = utils.getEnvValue('REDIS_HOST', '')
REDIS_PORT = int(utils.getEnvValue('REDIS_PORT', ''))
REDIS_PASS = utils.getEnvValue('REDIS_PASS', '')

if API_ENDPOINT_EMAIL_CONFIRM == None:
    raise Exception('Missing environment config: API_ENDPOINT_EMAIL_CONFIRM')

if GMAIL_ACCOUNT == None:
    raise Exception('Missing environment config: GMAIL_ACCOUNT')

if GMAIL_APP_PASSWORD == None:
    raise Exception('Missing environment config: GMAIL_APP_PASSWORD')

MongoCredential = Munch(host=MONGO_HOST, port=MONGO_PORT, user=MONGO_USER, passwd=MONGO_PASS)

ssoLogProvider = LogService(LogProviderMongo(MongoCredential, 'sso_api_log'))

accStorageService = AccountStorageService(AccountStorageProviderMongo(MongoCredential, 'accounts'))
accRepo = AccountRepository(accStorageService)

TokenRedisCredential = Munch(host=REDIS_HOST, port=REDIS_PORT, passwd=REDIS_PASS)

tokenStorageService = TokenStorageService(TokenStorageProviderRedis(ssoLogProvider, TokenRedisCredential))
tokenRepo = TokenRepository(defs.JWT_PRIVATE_KEY, JWT_ALGORITHM, tokenStorageService)
signInService = SignInService(ssoLogProvider, accRepo, tokenRepo)

emailService = ServiceFactory().createGmailService(GMAIL_ACCOUNT, GMAIL_APP_PASSWORD, GMAIL_ACCOUNT)
registrationValidator = RegistrationValidator(ssoLogProvider, accRepo, tokenRepo, emailService)

aaStorage = AuthAppStorageService(AuthAppStorageProviderMongo(ssoLogProvider, MongoCredential, 'oauth'))
aaRepo = AuthAppRepository(aaStorage)
oauthService = Oauth2(ssoLogProvider, aaRepo)

print('=============================')
print('SIMPLE SSO API')
print('=============================')

@app.get("/")
def welcome(request:Request):
    return 'welcome to Simple SSO'

@app.post("/api/v1/auth/registration/register")
def registration_register(model: account.RegistrationModel, send_activation_email:str = Header()):
    print('POST [/api/v1/auth/registration/register]')
    
    acc = account.fromRegistrationModel(model)
    result = accRepo.registerNewAccount(acc)
    if result.errCode == defs.ERRCODE_NONE:
        token = tokenRepo.createJWTToken({'account_id': result['account']['_id'], 'type': defs.TOKEN_TYPE_REGISTRATION_CONFIRM })
        if send_activation_email == '1':
            registrationValidator.sendValidateEmail(acc, token, API_ENDPOINT_EMAIL_CONFIRM)

        result = { 'errCode': defs.ERRCODE_NONE, 'token': token }
    return result

# @app.post("/register/phone")
# def register(model: account.RegistrationFormPhone):
#     return model

@app.get("/api/v1/auth/registration/validate/{token}")
def registration_validate_token(token):
    result = registrationValidator.validateConfirmCode(token)
    print('[register/validate/%s] result: %s' % (token, json.dumps(result.__dict__)))
    if result.errCode == defs.ERRCODE_NONE:
        return { 'errCode': defs.ERRCODE_NONE, 'msg': 'Congratulation! You can Login with your email now!' }
    return result

@app.post("/api/v1/auth/login")
def login(authorization:str = Header(), username:str = Form(), password: str = Form()):
    if authorization == None:
        raise HTTPException(status_code=400, detail="Missing authorization in header")

    if not authorization.startswith('Basic '):
        raise HTTPException(status_code=400, detail="Not support authorization=%s in header" % authorization)

    print(f'----------- authorization={authorization} username={username} password={password} ------------')

    authorization = authorization[6:]
    
    client_parts = base64.b64decode(authorization).decode('utf-8').split(':')
    app_code = client_parts[0]
    client_secret = client_parts[1]

    print(f'---- check login from client {app_code} secret {client_secret}...')

    if not oauthService.isClientValid(app_code, client_secret):
        raise HTTPException(status_code=400, detail="Invalid client authorization")
    
    return signInService.signIn(app_code, username, password)

@app.get("/api/v1/token/verify/{token}")
def token_verify(token, app_id:str = Header(convert_underscores=False)):
    if app_id == None:
        raise HTTPException(status_code=400, detail="app_id not exists in headers")

    metadata = tokenRepo.getToken(token)
    if metadata == None:
        ssoLogProvider.debug('api', { 'api': 'api/v1/token/verify/%s' % token, 'app_id': app_id, 'msg': 'token not found' }, state='failed')
        raise HTTPException(status_code=404, detail="Token not found")

    if metadata['app_id'] != app_id:
        ssoLogProvider.debug('api', { 'api': 'api/v1/token/verify/%s' % token, 'app_id': app_id, 'msg': 'metadata.app_id not match', 'token_app_id': metadata['app_id'] }, state='failed')
        return None
    return metadata

# @app.post("/api/v1/oauth2/login")
# def oauth2_login(authorization:str = Header(), grant_type: str = Form(), app_id:str = Header(convert_underscores=False), username:str = Form(), password: str = Form()):
#     if authorization == None:
#         raise HTTPException(status_code=400, detail="Missing authorization in header")

#     if not authorization.startswith('Basic '):
#         raise HTTPException(status_code=400, detail="Not support authorization=%s in header" % authorization)

#     authorization = authorization[6:]
#     client_parts = base64.b64decode(authorization).decode('utf-8').split(':')
#     client_key = client_parts[0]
#     client_secret = client_parts[1]
        
#     if not oauthService.isClientValid(app_id, client_key, client_secret):
#         raise HTTPException(status_code=400, detail="Invalid client authorization")
    
#     return signInService.signIn(app_id, LoginModel(emailOrPhone=username, password=password))
    
@app.get("/api/v1/application")
def app_get_client(id:Union[str, None] = None, code:Union[str, None]=None, apikey: str = Header()):
    if apikey != ADMIN_APIKEY:
        raise HTTPException(status_code=403, detail="Forbidden")

    if id != None:
        return aaRepo.getByAppID(id)
    elif code != None:
        return aaRepo.getByAppCode(code)
    return HTTPException(status_code=404, detail="App not found")

@app.put("/api/v1/application")
def app_add_client(model: AuthApplicationRegistrationModel, apikey: str = Header()):
    if apikey != ADMIN_APIKEY:
        raise HTTPException(status_code=403, detail="Forbidden")

    appInfo = AuthApplication.fromRegistrationModel(model)
    return aaRepo.add(appInfo)

@app.get("/api/v1/applications")
def app_get_clients(apikey: str = Header()):
    if apikey != ADMIN_APIKEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return aaRepo.getAll()

@app.delete("/api/v1/applications")
def app_delete_clients(apikey: str = Header()):
    if apikey != ADMIN_APIKEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return aaRepo.deleteAll()

@app.delete("/api/v1/accounts")
def accounts_delete_all(apikey: str = Header()):
    if apikey != ADMIN_APIKEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return accRepo.deleteAll()

@app.get("/api/v1/accounts")
def accounts_get_all(apikey: str = Header()):
    if apikey != ADMIN_APIKEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return accRepo.getAll()


@app.get("/api/v1/accounts/tenants")
def accounts_get_all_tenants(apikey: str = Header()):
    if apikey != ADMIN_APIKEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return accRepo.getAllTenants()

@app.post("/api/v1/account/{account_id}/upgrade/tenant")
def account_upgrade_to_tenant(account_id, apikey: str = Header()):
    if apikey != ADMIN_APIKEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    success = accRepo.upgradeToTenant(account_id)
    if success:
        return {'errCode': defs.ERRCODE_NONE, 'msg': f'Account {account_id} has been upgraded as a Tenant'}
    else:
        raise HTTPException(status_code=500, detail=f"Unhandled Error: can not upgrade account {account_id} as a Tenant")