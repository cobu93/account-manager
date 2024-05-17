from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    account_id: int
    op_date: datetime
    amount: float

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True