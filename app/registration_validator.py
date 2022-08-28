from re import S

from s_mail import EmailService
from s_log import LogService
from repo_account import AccountRepository
from repo_token import TokenRepository
from models import account as ModelAccount
import defs
class ValidateConfirmCodeResult():
    def __init__(self, errCode):
        self.errCode = errCode

class RegistrationValidator():
    def __init__(self, logService: LogService, accRepo:AccountRepository, tokenRepo:TokenRepository, emailService: EmailService):
        self.accRepo = accRepo
        self.tokenRepo = tokenRepo
        self.emailService = emailService
        self.logService = logService

    def validateConfirmCode(self, token):
        metadata = self.tokenRepo.getToken(token)
        if metadata == None:
            self.logService.error('RegistrationValidator', 'validateConfirmCode token=%s => Token not found' % (token))
            return ValidateConfirmCodeResult(errCode=defs.ERRCODE_CONFIRM_LINK_EXPIRED)

        accID = metadata['account_id']
        tokenType = metadata['type']
        if tokenType == defs.TOKEN_TYPE_REGISTRATION_CONFIRM:
            self.accRepo.updateAccount(accID, {'activated': True})
            self.logService.debug('RegistrationValidator', 'validateConfirmCode token=%s => Token not found' % (token), state='success')
            return ValidateConfirmCodeResult(errCode=defs.ERRCODE_NONE)
        else:
            self.logService.error('RegistrationValidator', 'validateConfirmCode token=%s => invalid token type: %s' % (token, tokenType))
            return ValidateConfirmCodeResult(errCode=defs.ERRCODE_BAD_REQUEST)

    def sendValidateEmail(self, account : ModelAccount.Account, token, endpoint):
        print('send validate email to ', account.email)
        url = '{endpoint}/api/v1/auth/registration/validate/{token}'.format(endpoint=endpoint, token=token)
        html = """
        <h1>SSO Registration Confirm</h1>
        <a href="{url}">{url}</a>
        """.format(url=url)
        self.emailService.send(account.email, 'SSO Registration confirm', html)