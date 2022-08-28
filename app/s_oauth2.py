from s_log import LogService
from repo_auth_app import AuthAppRepository
class Oauth2():
    def __init__(self, logger: LogService, repo: AuthAppRepository):
        self.repo = repo
        self.logger = logger

    def isClientValid(self, app_code, client_secret):
        print('Oauth2 check client: %s:%s' % (app_code, client_secret))
        client = self.repo.getByAppCode(app_code)
        print('get client by app code: ', app_code)
        print(client)
        if client == None: 
            self.logger.info('Oauth2', { 'action': 'check client valid', 'app_code': app_code, 'result': 'client not exists' })
            return False

        if client['client_secret'] == client_secret:
            return True
        else:
            self.logger.debug('Oauth2', { 'action': 'check client valid', 'app_code': app_code, 'client_secret': client_secret, 'result': 'client_secret not match' })
        return False