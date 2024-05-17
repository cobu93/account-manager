from typing import List
from fastapi import FastAPI, Depends, UploadFile
from sqlalchemy.orm import Session
import schemas
from conn import aws, db

from db import Account, Transaction

import utils.file
import utils.report

import os


app = FastAPI()

@app.get("/accounts", response_model=List[schemas.Account])
def list_accounts(db_sess: Session = Depends(db.get_session)):
    """
    List the existing accounts.
    """
    return Account.list(db_sess)

@app.get("/account/{id}", response_model=schemas.Account)
def get_account(id: int, db_sess: Session = Depends(db.get_session)):
    """
    Get the account information related to the specified id.
    """
    return Account.get(id, db_sess)

@app.post("/account", response_model=schemas.Account)
def create_account(account: schemas.CreateAccount, db_sess: Session = Depends(db.get_session)):
    """
    Creates a new account
    """
    return Account.create(account, db_sess)

# This is a helper function for developing
@app.post("/transactions/upload", response_model=schemas.GenericResponse)
def upload_transactions(file: UploadFile, s3_cli = Depends(aws.get_s3_client)):
    """
    Upload a transactions file to a S3 default bucket. 
    
    The S3 default bucket is given by:
    - *bucket*: "account-manager"
    - *path*: "."
    - *file_name*: The same name as the file uploaded
    """
    return utils.file.upload_obj_to_s3(
                "account-manager",
                os.path.join(".", file.filename),
                file.file,
                s3_cli
            )

@app.post("/account/{id}/transactions/save-file", response_model=schemas.GenericResponse)
def save_transactions(id: int, desc: schemas.S3FileDescription, db_sess: Session = Depends(db.get_session), s3_cli = Depends(aws.get_s3_client)):
    """
    Save an existing transaction file into the S3 bucket to the database.

    The uploaded transactions will be associated with the given account id.
    """
    return Transaction.save_file(id, desc, db_sess, s3_cli)


@app.post("/account/{id}/send-report", response_model=schemas.GenericResponse)
def send_report_account(id: int, db_sess: Session = Depends(db.get_session)):
    """
    Retrieve the transactions associated to an account and create a summary of them.

    The summary is then sent to the email associated to the account.
    """
    acc = Account.get(id, db_sess)
    return utils.report.send_report(acc.email, acc.transactions)

        
    
        
