
from pydantic import BaseModel
class RegistrationModel(BaseModel):
    id: str
    email: str
    phone: str
    name: str
    password: str
    address: str

class Account():
    def __init__(self, id, name, mail, phone, address, passhash, activated):
        self.id = id
        self.name = name
        self.phone = phone
        self.address =address
        self.passhash = passhash
        self.activated = activated

def createPasshash(password):
    return password

def fromRegistrationModel(model: RegistrationModel):
    return Account(id=model.id, name=model.name, mail=model.email, phone=model.phone, address=model.address, activated=False, passhash=createPasshash(model.password))