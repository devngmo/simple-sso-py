from munch import Munch
import utils, defs
from models import account as ModelAccount
from models.auth_app import AuthApplication
from s_auth_app_storage import AuthAppStorageService

class AuthAppRepository():
    def __init__(self, storage: AuthAppStorageService):
        self.storage = storage
    
    def add(self, appInfo: AuthApplication):
        client = self.storage.getByAppCode(appInfo.code)
        if client != None:
            return { 'errCode': defs.ERRCODE_CLIENT_ALREADY_EXISTS }
        
        app_id = self.storage.add(appInfo)
        return { 'errCode': defs.ERRCODE_NONE, 'app_id': app_id }

    def getByAppID(self, app_id):
        return self.storage.getByAppID(app_id)

    def getByAppCode(self, app_code):
        return self.storage.getByAppCode(app_code)

    def getAll(self):
        return self.storage.getAll()

    def deleteAll(self):
        return self.storage.deleteAll()