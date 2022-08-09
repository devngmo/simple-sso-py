class EmailService():
    def __init__(self, serviceProvider):
        self.serviceProvider = serviceProvider

    def send(self, recipient, subject, body):
        self.serviceProvider.send(recipient, subject, body)
        