from db import Transaction
from typing import List
import pandas as pd
from .email import send_email
from jinja2 import Template
import base64

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
    data = []

    for t in transactions:
        
        data.append({
            "date": t.op_date,
            "amount": t.amount,
        })

    report_df = pd.DataFrame(data)
    report_df["date"] = pd.to_datetime(report_df["date"])

    total_balance = report_df["amount"].sum()
    average_credit = report_df.query("amount > 0")["amount"].mean()
    average_debit = report_df.query("amount < 0")["amount"].mean()
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

    report = build_report(transactions)

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
