import os, sys, json

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_DIR)
sys.path.append(os.path.dirname(APP_DIR))

print(__package__)

import defs
from models import account
from fastapi import FastAPI, Request


API_ENDPOINT_EMAIL_CONFIRM = os.environ['API_ENDPOINT_EMAIL_CONFIRM']



from s_factory import ServiceFactory
from s_mail import EmailService
from s_token_storage import TokenStorageService
from sp_in_memory_storage import InMemoryStorageProvider
from s_auth import AutheticationService, LoginModel
from s_acc_storage import AccountStorageService
from repo_account import AccountRepository
from repo_token import TokenRepository

from registration_validator import RegistrationValidator

app = FastAPI()

docStorageProvider = InMemoryStorageProvider()

accStorageService = AccountStorageService(docStorageProvider)
accRepo = AccountRepository(accStorageService)

tokenStorageService = TokenStorageService(docStorageProvider)
tokenRepo = TokenRepository(tokenStorageService)
authService = AutheticationService(accRepo, tokenRepo)

GMAIL_ACCOUNT = os.environ['GMAIL_ACCOUNT']
GMAIL_APP_PASSWORD = os.environ['GMAIL_APP_PASSWORD']
emailService = ServiceFactory().createGmailService(GMAIL_ACCOUNT, GMAIL_APP_PASSWORD, GMAIL_ACCOUNT)
registrationValidator = RegistrationValidator(accRepo, tokenRepo, emailService)
print('=============================')
print('SIMPLE SSO API')
print('  Storage Provider: %s' % docStorageProvider)
print('=============================')


@app.get("/")
def welcome(request:Request):
    return 'welcome to Simple SSO'

@app.post("/register")
def register(model: account.RegistrationModel, request: Request):
    print('API [/register]')
    acc = account.fromRegistrationModel(model)
    result = accRepo.registerNewAccount(acc)
    if result.errCode == defs.ERRCODE_NONE:
        token = tokenRepo.createToken({ 'id': acc.id, 'type':'registration-confirm-token' })
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
def register(token):
    result = registrationValidator.validateConfirmCode(token)
    print('[register/validate/%s] result: %s' % (token, json.dumps(result.__dict__)))
    return result

@app.post("/login")
def login(model: LoginModel):
    return authService.login(model)

@app.post("/token/verify/{token}")
def login(token):
    return tokenRepo.get(token)

