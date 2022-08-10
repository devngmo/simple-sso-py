import base64

import os, sys, json
import uuid


APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_DIR)
sys.path.append(os.path.dirname(APP_DIR))
 
import defs
from models import account
from fastapi import FastAPI, Request, Depends, Form, Header, HTTPException

from s_client_storage import OauthClientStorageService
from s_oauth2 import Oauth2
from s_signin import LoginModel, SignInService
from s_factory import ServiceFactory
from s_mail import EmailService
from s_token_storage import TokenStorageService
from sp_in_memory_storage import InMemoryStorageProvider
from s_acc_storage import AccountStorageService
from repo_account import AccountRepository
from repo_token import TokenRepository
from repo_client import OauthClientRepository
from registration_validator import RegistrationValidator

app = FastAPI()


ADMIN_APIKEY = os.environ['ADMIN_APIKEY']
API_ENDPOINT_EMAIL_CONFIRM = os.environ['API_ENDPOINT_EMAIL_CONFIRM']

docStorageProvider = InMemoryStorageProvider()

accStorageService = AccountStorageService(docStorageProvider)
accRepo = AccountRepository(accStorageService)

tokenStorageService = TokenStorageService(docStorageProvider)
tokenRepo = TokenRepository(tokenStorageService)
signInService = SignInService(accRepo, tokenRepo)

GMAIL_ACCOUNT = os.environ['GMAIL_ACCOUNT']
GMAIL_APP_PASSWORD = os.environ['GMAIL_APP_PASSWORD']
emailService = ServiceFactory().createGmailService(GMAIL_ACCOUNT, GMAIL_APP_PASSWORD, GMAIL_ACCOUNT)
registrationValidator = RegistrationValidator(accRepo, tokenRepo, emailService)


clientStorage = OauthClientStorageService(storageProvider=docStorageProvider)
clientRepo = OauthClientRepository(clientStorage=clientStorage)
oauthService = Oauth2(clientRepo)

print('=============================')
print('SIMPLE SSO API')
print('  Storage Provider: %s' % docStorageProvider)
print('=============================')


@app.get("/")
def welcome(request:Request):
    return 'welcome to Simple SSO'

@app.post("/register")
def register(model: account.RegistrationModel, client_id: str = Header()):
    print('API [/register]')
    if client_id == None:
        raise HTTPException(status_code=400, detail="client_id not exists in headers")
    
    acc = account.fromRegistrationModel(model)
    result = accRepo.registerNewAccount(client_id, acc)
    if result.errCode == defs.ERRCODE_NONE:
        token = tokenRepo.createToken({'client_id':client_id, 'id': acc.id, 'type':'registration-confirm-token' })
        registrationValidator.sendValidateEmail(acc, token, API_ENDPOINT_EMAIL_CONFIRM)

        result = { 'errCode': defs.ERRCODE_NONE }
        print('register result: %s' % json.dumps(result))
        return result
    else:
        print('register result: %s' % json.dumps(result))
        return result

# @app.post("/register/phone")
# def register(model: account.RegistrationFormPhone):
#     return model

@app.get("/register/validate/{token}")
def register_validate_token(token):
    result = registrationValidator.validateConfirmCode(token)
    print('[register/validate/%s] result: %s' % (token, json.dumps(result.__dict__)))
    return result

@app.post("/login")
def login(model: LoginModel, client_id: str = Header()):
    if client_id == None:
        raise HTTPException(status_code=400, detail="client_id not exists in headers")

    return signInService.signIn(client_id, model)

@app.get("/token/verify/{token}")
def token_verify(token, client_id: str = Header()):
    if client_id == None:
        raise HTTPException(status_code=400, detail="client_id not exists in headers")

    metadata = tokenRepo.get(token)
    if metadata == None:
        raise HTTPException(status_code=404, detail="Token not found")

    if metadata['client_id'] == client_id:
        return metadata
    
    raise HTTPException(status_code=404, detail="Token not found")

@app.post("/oauth2/token")
def oauth2_token(authorization:str = Header(), grant_type: str = Form(), username:str = Form(), password: str = Form()):
    if authorization == None:
        raise HTTPException(status_code=400, detail="Missing authorization in header")

    if not authorization.startswith('Basic '):
        raise HTTPException(status_code=400, detail="Not support authorization=%s in header" % auth)

    authorization = authorization[6:]
    client_parts = base64.b64decode(authorization).decode('utf-8').split(':')
    client_id = client_parts[0]
    client_secret = client_parts[1]
    
    if not oauthService.isClientValid(client_id, client_secret):
        raise HTTPException(status_code=400, detail="Invalid client authorization")
    
    return signInService.signIn(client_id, LoginModel(username, password))
    


@app.get("oauth2/token/verify/{token}")
def token_verify(token, client_id: str = Header()):
    if client_id == None:
        raise HTTPException(status_code=400, detail="client_id not exists in headers")

    metadata = tokenRepo.getClientToken(client_id, token)
    if metadata == None:
        raise HTTPException(status_code=404, detail="Token not found")

    return metadata

@app.put("oauth2/client/{id}/{secret}")
def oauth2_add_client(id, secret, apikey: str = Header()):
    if apikey != ADMIN_APIKEY:
        raise HTTPException(status_code=403, detail="Forbidden")

    clientRepo.add(id, secret)
    return 'ok'

@app.get("oauth2/clients")
def oauth2_get_clients(apikey: str = Header()):
    if apikey != ADMIN_APIKEY:
        raise HTTPException(status_code=403, detail="Forbidden")

    return clientRepo.getAll()


@app.get('/dev/accounts')
def get_all_accounts(client_id:str = Header(), apikey: str = Header()):
    if apikey != ADMIN_APIKEY:
        raise HTTPException(status_code=403, detail="Forbidden")

    if client_id == None:
        raise HTTPException(status_code=400, detail="client_id not exists in headers")
    
    return accRepo.getAll(client_id)
