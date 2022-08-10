import smtplib

from s_mail import EmailService
from sp_smtp_email import SMPTEmailProvider
class ServiceFactory():
    def createGmailService(self, username, password, defaultFrom):
        return EmailService(SMPTEmailProvider(username, password, defaultFrom, "smtp.gmail.com", 587))