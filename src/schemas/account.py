from pydantic import BaseModel

class AccountBase(BaseModel):
    email: str

class CreateAccount(AccountBase):
    pass

class Account(AccountBase):
    id: int
    
    class Config:
        from_attributes = True