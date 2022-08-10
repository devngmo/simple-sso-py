from re import S
from s_mail import EmailService
from repo_account import AccountRepository
from repo_token import TokenRepository
from models import account as ModelAccount
import defs
class ValidateConfirmCodeResult():
    def __init__(self, errorCode):
        self.errorCode = errorCode

class RegistrationValidator():
    def __init__(self, accRepo:AccountRepository, tokenRepo:TokenRepository, emailService: EmailService):
        self.accRepo = accRepo
        self.tokenRepo = tokenRepo
        self.emailService = emailService

    def validateConfirmCode(self, token):
        print('[RegistrationValidator] validate confirm code: %s' % token)
        metadata = self.tokenRepo.get(token)
        if metadata == None:
            print('[RegistrationValidator] CONFIRM TOKEN not found')
            return ValidateConfirmCodeResult(errorCode=defs.ERRCODE_CONFIRM_LINK_EXPIRED)

        accID = metadata['id']
        acc = self.accRepo.finByID(accID)
        acc['activated'] = True
        self.accRepo.updateAccount(acc)
        print('[RegistrationValidator] Account %s was ACTIVATED' % acc['id'])
        return ValidateConfirmCodeResult(errorCode=defs.ERRCODE_NONE)
    
    def sendValidateEmail(self, account : ModelAccount.Account, token):
        url = 'http://localhost:8000/register/validate/{token}'.format(token=token)
        html = """
        <h1>SSO Registration Confirm</h1>
        <a href="{url}">{url}</a>
        """.format(url=url)
        self.emailService.send(account.email, 'SSO Registration confirm', html)