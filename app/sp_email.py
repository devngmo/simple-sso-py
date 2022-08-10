import smtplib
class EmailServiceProvider():
    def __init__(self, username, password, defaultFrom):
        self.username = username
        self.password = password
        self.defaultFrom = defaultFrom

    def send(self, recipient, subject, body):
        pass