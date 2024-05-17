import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from typing import List

def send_email(
        subject: str, 
        body: str, 
        sender: str, 
        recipients: List[str],
        password: str,
        smtp_server: str,
        smtp_port: int,
        logo: str
    ):

    """
    Builds the request for sending an email.
    """

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ",".join(recipients)
    msg.attach(MIMEText(body, "html"))
    
    # Attach a logo in the mail
    if logo:
        with open(logo, "rb") as f:
            logo_img = MIMEImage(f.read())

        logo_img.add_header("Content-ID", "<logo>")
        msg.attach(logo_img)


    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
    except Exception as e:
        return dict(message=str(e), code=-1)
    
    return dict(message="Email sent", code=0)