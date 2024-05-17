from pydantic import BaseModel
from pydantic import EmailStr, Field

class AccountBase(BaseModel):
    email: EmailStr

class CreateAccount(AccountBase):
    pass

class Account(AccountBase):
    id: int
    
    class Config:
        from_attributes = True