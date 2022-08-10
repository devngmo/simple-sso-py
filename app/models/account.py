
import json
from pydantic import BaseModel
class RegistrationModel(BaseModel):
    id: str
    email: str
    phone: str
    name: str
    password: str
    address: str

class Account():
    def __init__(self, id, name, email, phone, address, passhash, activated):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address =address
        self.passhash = passhash
        self.activated = activated

    def toJSON(self):
        return json.dumps(self, default=lambda o : o.__dict__, sort_keys=True, indent=4)

def createPasshash(password):
    return password

def fromRegistrationModel(model: RegistrationModel):
    return Account(id=model.id, name=model.name, email=model.email, phone=model.phone, address=model.address, activated=False, passhash=createPasshash(model.password))