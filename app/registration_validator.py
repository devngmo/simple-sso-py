import iniconfig
from repositories.account_repo import AccountRepository
from repositories.token_repo import TokenRepository
from services.mail import EmailService
import defs
class ValidateConfirmCodeResult():
    def __init__(self, errorCode):
        self.errorCode = errorCode

class RegistrationValidator():
    def __init__(self, accRepo:AccountRepository, tokenRepo:TokenRepository, emailService):
        self.accRepo = accRepo
        self.tokenRepo = tokenRepo
    def validateConfirmCode(self, token):
        metadata = self.tokenRepo.get(token)
        accID = metadata['id']
        acc = self.accRepo.finByID(accID)
        acc['activated'] = True
        self.accRepo.updateAccount(acc)
        return ValidateConfirmCodeResult(errorCode=defs.ERRCODE_CONFIRM_LINK_EXPIRED)
    
    def sendValidateEmail(self, account, token):
        html = """
        <h1>SSO Registration Confirm</h1>
        <a href="http://localhost:8000">{token}</a>
        """.format(token=token)
        emailService.send(account.email, 'SSO Registration confirm', html)