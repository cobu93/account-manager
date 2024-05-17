from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.orm import Session

from .base import Base
from .transaction import Transaction
from ..conn import db

import app.schemas as schemas

class Account(Base):

    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100))
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="account", cascade="all")
    
    def __repr__(self) -> str:
        return f"Account(id={self.id}, email={self.email})"
    
    @staticmethod
    def list(db_sess: Session, limit:int =1000):
        return db_sess.query(Account).limit(limit).all()
    
    @staticmethod
    def get(id: int, db_sess: Session):
        return db_sess.query(Account).get(id)
        
    
    @staticmethod
    def create(account: schemas.CreateAccount, db_sess: Session):
        db_account = Account(email=account.email)
        db_sess.add(db_account)
        db_sess.commit()
        db_sess.refresh(db_account)
        return db_account


