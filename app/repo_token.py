from datetime import datetime, timedelta
from typing import Union
import uuid
from passlib.context import CryptContext
from jose import JWTError, jwt

from s_token_storage import TokenStorageService

class TokenRepository():
    def __init__(self, jwtSecretKey, jwtAlgorithm, tokenStorage: TokenStorageService):
        self.tokenStorage = tokenStorage
        self.jwtSecretKey = jwtSecretKey
        self.jwtAlgorithm = jwtAlgorithm
        self.pwdContext = CryptContext(schemes='bcrypt', deprecated='auto')

    def addToken(self, token, metadata):
        self.tokenStorage.addToken(token, metadata)

    def getToken(self, token):
        return self.tokenStorage.getToken(token)

    def createJWTToken(self, metadata:dict, expires_delta: Union[timedelta, None] = None):
        to_encode = metadata.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        print('JWT create token expire: ', expire.isoformat())
        to_encode.update({'exp': expire})
        token = jwt.encode(to_encode, self.jwtSecretKey, algorithm=self.jwtAlgorithm)
        self.addToken(token, metadata)
        return token

    def createUUIDToken(self, metadata):
        token = uuid.uuid4().hex
        self.addToken(token, metadata)
        return token

    