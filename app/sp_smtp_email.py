import smtplib

from sp_email import EmailServiceProvider
class SMPTEmailProvider(EmailServiceProvider):
    def __init__(self, username, password, defaultFrom, smtpHost, smtpPort):
        self.username = username
        self.password = password
        self.defaultFrom = defaultFrom
        self.smtpHost = smtpHost
        self.smtpPort = smtpPort

    def send(self, recipient, subject, body):
        FROM = self.defaultFrom
        TO = recipient if isinstance(recipient, list) else [recipient]
        SUBJECT = subject
        TEXT = body

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP(self.smtpHost, self.smtpPort)
            server.ehlo()
            server.starttls()
            print('SMTP Login %s:%d with account: %s %s' % (self.smtpHost, self.smtpPort, self.username, self.password))
            server.login(self.username, self.password)
            server.sendmail(FROM, TO, message)
            server.close()
            print ('successfully sent the mail')
        except Exception as ex:
            print ("failed to send mail: %s" % ex)