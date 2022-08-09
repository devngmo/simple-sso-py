import smtplib
class GMailServiceProvider():
    def __init__(self, username, password, defaultFrom):
        self.username = username
        self.password = password
        self.defaultFrom = defaultFrom

    def send(self, recipient, subject, body):
        FROM = self.defaultFrom
        TO = recipient if isinstance(recipient, list) else [recipient]
        SUBJECT = subject
        TEXT = body

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(FROM, TO, message)
            server.close()
            print ('successfully sent the mail')
        except:
            print ("failed to send mail")