from sp_email import EmailServiceProvider
class EmailService():
    def __init__(self, serviceProvider:EmailServiceProvider):
        self.serviceProvider = serviceProvider

    def send(self, recipient, subject, body):
        self.serviceProvider.send(recipient, subject, body)
        