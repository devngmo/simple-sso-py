import os, sys, defs, utils
from models import account
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_DIR)

print(__package__)

from providers.gmail import GMailServiceProvider
from services.mail import EmailService
from services.token_storage_service import TokenStorageService
from providers.in_memory_storage_provider import InMemoryStorageProvider
from services.auth import AutheticationService, LoginModel
from services.acc_storage_service import AccountStorageService
from repositories.account_repo import AccountRepository
from repositories.token_repo import TokenRepository

from registration_validator import RegistrationValidator

app = FastAPI()

docStorageProvider = InMemoryStorageProvider()

accStorageService = AccountStorageService(docStorageProvider)
accRepo = AccountRepository(accStorageService)

tokenStorageService = TokenStorageService(docStorageProvider)
tokenRepo = TokenRepository(tokenStorageService)
authService = AutheticationService(accRepo, tokenRepo)

emailService = EmailService(GMailServiceProvider('tmlfun@gmail.com', 'Qwert@12345!', 'tmlfun@gmail.com'))
registrationValidator = RegistrationValidator(accRepo, tokenRepo, emailService)
print('=============================')
print('SIMPLE SSO API')
print('  Storage Provider: %s' % docStorageProvider)
print('=============================')


@app.get("/")
def welcome():
    return 'welcome to Simple SSO'

@app.post("/register")
def register(model: account.RegistrationModel):
    acc = account.fromRegistrationModel(model)
    result = accRepo.registerNewAccount(acc)
    if result.errCode == defs.ERRCODE_NONE:
        token = tokenRepo.createToken({ 'id': acc.id, 'type':'registration-confirm-token' })
        registrationValidator.sendValidateEmail(acc, token)
        return { 'errCode': defs.ERRCODE_NONE }
    else:
        return result

# @app.post("/register/phone")
# def register(model: account.RegistrationFormPhone):
#     return model

@app.post("/register/validate/{code}")
def register(code):
    result = registrationValidator.validateConfirmCode(code)
    return result

@app.post("/login")
def login(model: LoginModel):
    return authService.login(model)

@app.post("/token/verify/{token}")
def login(token):
    return tokenRepo.get(token) != None

