
import json, os, defs
from pydantic import BaseModel
from passlib.hash import pbkdf2_sha256


class RegistrationModel(BaseModel):
    email: str
    phone: str
    name: str
    password: str
    address: str

class Account():
    def __init__(self, name, email, phone, address, passhash, activated, is_tenant, parent_tenant_id):
        self.name = name
        self.email = email
        self.phone = phone
        self.address =address
        self.passhash = passhash
        self.activated = activated
        self.is_tenant = is_tenant
        self.parent_tenant_id = parent_tenant_id

    def toJSON(self):
        return json.dumps(self, default=lambda o : o.__dict__, sort_keys=True, indent=4)

    def toDict(self):
        return self.__dict__

def createPasshash(password):
    return pbkdf2_sha256.hash(password)

def fromRegistrationModel(model: RegistrationModel):
    return Account(name=model.name, email=model.email, phone=model.phone, address=model.address, activated=False, passhash=createPasshash(model.password), is_tenant=False, parent_tenant_id=None)