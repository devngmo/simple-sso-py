from datetime import datetime, timedelta
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

    def add(self, token, metadata):
        self.tokenStorage.addToken(token, metadata)

    def get(self, token):
        return self.tokenStorage.get(token)

    def createToken(self, metadata:dict, expires_delta: timedelta | None = None):
        to_encode = metadata.copy()
        if expires_delta:
            exprire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({'exp': expire})
        token = jwt.encode(to_encode, self.jwtSecretKey, algorithm=self.jwtAlgorithm)
        self.add(token, metadata)
        return token

    def addClientToken(self, client_id, token, metadata):
        self.tokenStorage.addClientToken(client_id, token, metadata)

    def getClientToken(self, client_id, token):
        return self.tokenStorage.getClientToken(client_id, token)

    def createClientToken(self, client_id, metadata):
        token = uuid.uuid4().hex
        self.addClientToken(client_id, token, metadata)
        return token

    