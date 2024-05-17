import os

DB_USER = os.environ["DB_USER"]
DB_NAME = os.environ["DB_NAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]

S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
BOTO3_ENDPOINT = os.environ.get("BOTO3_ENDPOINT", None)

REPORT_SUBJECT = "Your account report!"
REPORT_BODY_TEMPLATE = "./assets/report/template.html"
REPORT_SMTP_SERVER = os.environ["REPORT_SMTP_SERVER"]
REPORT_SMTP_PORT = os.environ["REPORT_SMTP_PORT"]
REPORT_EMAIL = os.environ["REPORT_EMAIL"]
REPORT_EMAIL_PASSWORD = os.environ["REPORT_EMAIL_PASSWORD"]