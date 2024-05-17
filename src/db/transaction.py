from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
import tempfile
import pandas as pd

import os

import utils.file
import utils.date

import schemas

from .base import Base

class Transaction(Base):
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    op_date: Mapped[datetime]
    amount: Mapped[float]
    account: Mapped["Account"] = relationship(back_populates="transactions")
    
    def __repr__(self) -> str:
        return f"Transaction(id={self.id}, account={self.account_id}, op_date={self.op_date}, amount={self.amount})"
    
    @staticmethod
    def save_file(account_id: int, file: schemas.S3FileDescription, db_sess: Session,  s3_cli):
        try:
            stream = tempfile.SpooledTemporaryFile()

            utils.file.download_obj_from_s3(
                file.bucket, 
                os.path.join(file.path, file.file_name), 
                stream, 
                s3_cli
            )

            stream._file.seek(0)
            df = pd.read_csv(stream._file)
            df["Date"] = df["Date"].apply(utils.date.parse_file_date)

            transactions = []
            for t in df.iloc:
                transactions.append(
                    Transaction(
                        id=t["Id"],
                        account_id=account_id,
                        op_date=t["Date"],
                        amount=t["Transaction"]
                    )
                )

            
            db_sess.bulk_save_objects(transactions)
            db_sess.commit()
            stream.close()

        except Exception as e:
            return dict(code=-1, message=str(e))

        return dict(code=0, message="Saved file")