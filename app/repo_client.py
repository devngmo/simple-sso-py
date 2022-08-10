from munch import Munch
import utils, defs
from models import account as ModelAccount
from s_client_storage import OauthClientStorageService

class OauthClientRepository():
    def __init__(self, clientStorage: OauthClientStorageService):
        self.clientStorage = clientStorage
    
    def add(self, clientID, clientSecret):
        c = self.clientStorage.findByID(clientID)
        if c != None:
            return { 'errCode': defs.ERRCODE_CLIENT_ALREADY_EXISTS }
        
        self.clientStorage.add(clientID, clientSecret)
        return { 'errCode': defs.ERRCODE_NONE }

    def find(self, clientID, clientSecret):
        return self.clientStorage.find(clientID, clientSecret)