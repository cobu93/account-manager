from db import Transaction
from typing import List
import pandas as pd
from .email import send_email
from jinja2 import Template
import base64
import numpy as np

from collections import namedtuple

from config import (REPORT_SUBJECT,
                    REPORT_BODY_TEMPLATE,
                    REPORT_SMTP_SERVER,
                    REPORT_SMTP_PORT,
                    REPORT_EMAIL,
                    REPORT_EMAIL_PASSWORD
                )

ReportInformation = namedtuple(
                        "ReportInformation", [
                            "total_balance",
                            "average_credit",
                            "average_debit",
                            "transactions_month"
                    ])

MonthlyTransactions = namedtuple(
                        "MonthlyTransaction", [
                            "month",
                            "count"
                    ])

def build_report(transactions: Transaction):
    """
    Extract the report information depending on the transactions.
    """

    data = []

    for t in transactions:
        
        data.append({
            "date": t.op_date,
            "amount": t.amount,
        })

    if len(data) <= 0:
        return None
    
    report_df = pd.DataFrame(data)
    report_df["date"] = pd.to_datetime(report_df["date"])

    total_balance = np.round(report_df["amount"].sum(), decimals=2)
    average_credit = np.round(report_df.query("amount > 0")["amount"].mean(), decimals=2)
    average_debit = np.round(report_df.query("amount < 0")["amount"].mean(), decimals=2)
    transactions_month = report_df.groupby(pd.Grouper(key="date", freq="ME")).count().reset_index()

    report = ReportInformation(total_balance, average_credit, average_debit, [])

    for tm in transactions_month.iloc:
        mt = MonthlyTransactions(
                tm["date"].strftime("%B"), 
                tm["amount"]
            )
        
        report.transactions_month.append(mt)
                
    return report


def send_report(
        email: str, 
        transactions: List[Transaction], 
        logo: str = "assets/logo.jpg"
    ):

    """
    Send the transactions report via email.
    """
    
    report = build_report(transactions)

    if not report:
        return dict(message="Nothing to be send", code=-3)

    # Read the predefined template and formats it
    with open(REPORT_BODY_TEMPLATE, "r") as f:
        template = Template(f.read())

    body = template.render(report._asdict())

    return send_email(
        subject=REPORT_SUBJECT, 
        body=body, 
        sender=REPORT_EMAIL,
        recipients=[email],
        password=REPORT_EMAIL_PASSWORD,
        smtp_server=REPORT_SMTP_SERVER,
        smtp_port=REPORT_SMTP_PORT,
        logo=logo
    )
