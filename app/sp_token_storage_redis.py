import json
import redis
import redis_helper
from s_log import LogService
from s_token_storage import TokenStorageProviderInterface

class TokenStorageProviderRedis(TokenStorageProviderInterface):
    def __init__(self, logger: LogService, credential):
        self.client = redis_helper.initClient(credential)
        self.logger = logger
        
    def addToken(self, token, metadata):
        if isinstance(metadata, dict) or isinstance(metadata, object):
            metaStr = json.dumps(metadata)
            self.logger.info('TokenStorageProviderRedis', 'add json token %s=%s' % (token, metaStr))
            self.client.set(token, metaStr)
        else:
            self.logger.info('TokenStorageProviderRedis', 'add value token %s=%s' % (token, metadata))
            self.client.set(token, metadata)

    def getToken(self, token):
        jsonStr = self.client.get(token)
        return json.loads(jsonStr)