from ctypes import util
import os, utils
ERRCODE_NONE = 'ERRCODE_NONE'
ERRCODE_BAD_REQUEST = 'ERRCODE_BAD_REQUEST'
ERRCODE_CONFIRM_LINK_EXPIRED = 'ERRCODE_CONFIRM_LINK_EXPIRED'
ERRCODE_REGISTER_EMAIL_ALREADY_EXIST = 'ERRCODE_REGISTER_EMAIL_ALREADY_EXIST'
ERRCODE_REGISTER_PHONE_ALREADY_EXIST = 'ERRCODE_REGISTER_PHONE_ALREADY_EXIST'

ERRCODE_CLIENT_ALREADY_EXISTS = 'ERRCODE_CLIENT_ALREADY_EXISTS'


TOKEN_TYPE_REGISTRATION_CONFIRM = 'registration-confirm-token'
TOKEN_TYPE_AUTH_ACCESS = 'auth-access-token'


tags_metadata = [
    {
        'name': 'accounts',
        'description': 'Operations with Accounts: Register/ Login / Logout'
    },
    {
        'name': 'token',
        'description': 'Operations with Token: Create / verify'
    },
    {
        'name': 'oauth',
        'description': 'Operations with OAuth: SignIn'
    }
]

DATA_FOLDER=os.path.join(os.getcwd(), 'data')
if not os.path.exists(DATA_FOLDER):
    print('ERROR: Data Folder not found: ', DATA_FOLDER)
jwtFilePath = os.path.join(DATA_FOLDER, 'jwt-key')
JWT_PRIVATE_KEY=''
if os.path.exists(jwtFilePath):
    JWT_PRIVATE_KEY = utils.loadText()
else:
    print('ERROR: File not found: ', jwtFilePath)