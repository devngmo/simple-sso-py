
import json
import uuid
from pydantic import BaseModel
#
# CLIENT is an Application which connect to SSO
#
class AuthApplicationRegistrationModel(BaseModel):
    code: str
    name: str
    desc: str
    client_secret: str

class AuthApplication():
    def __init__(self, id, code, name, desc, client_secret, is_active):
        self._id = id
        self.code = code
        self.name = name
        self.desc = desc
        self.client_secret = client_secret
        self.is_active = is_active

    def fromRegistrationModel(model: AuthApplicationRegistrationModel):
        user_id = uuid.uuid4().hex
        return AuthApplication(user_id, model.code, model.name, model.desc, model.client_secret, is_active=True)

    def toJSON(self):
        return json.dumps(self, default=lambda o : o.__dict__, sort_keys=True, indent=4)

    def toDict(self):
        return self.__dict__