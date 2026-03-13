import smtplib
from email.message import EmailMessage
import os

from utils.email_template import build_email_body


def send_email_report(metadata, excel_file, sender_email, sender_password, receiver_email):

    subject = "Daily Job Intelligence Report"

    body = build_email_body(metadata)

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(body)

    if os.path.exists(excel_file):

        with open(excel_file, "rb") as f:
            file_data = f.read()

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=os.path.basename(excel_file)
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(sender_email, sender_password)

        smtp.send_message(msg)

    print("Email report sent successfully")