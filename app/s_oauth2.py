class Oauth2():
    def __init__(self, clientRepo):
        self.clientRepo = clientRepo

    def isClientValid(self, clientID, clientSecret):
        c = self.clientRepo.find(clientID, clientSecret)
        return c != None