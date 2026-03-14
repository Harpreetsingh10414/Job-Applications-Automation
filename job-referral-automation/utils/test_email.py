import smtplib
import sys
import os
from email.message import EmailMessage

# allow import from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import EMAIL_CONFIG


def send_test_email():

    sender = EMAIL_CONFIG["sender_email"]
    receiver = EMAIL_CONFIG["receiver_email"]
    password = EMAIL_CONFIG["app_password"]

    msg = EmailMessage()

    msg["Subject"] = "Test Email - Job Automation System"
    msg["From"] = sender
    msg["To"] = receiver

    msg.set_content("""
Hello,

This is a test email from the Job Intelligence Automation System.

If you received this email, the email functionality is working correctly.

Regards,
Job Automation System
""")

    try:

        print("Connecting to Gmail SMTP...")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(sender, password)

            smtp.send_message(msg)

        print("✅ Test email sent successfully!")

    except Exception as e:

        print("❌ Failed to send email")
        print(e)


if __name__ == "__main__":
    send_test_email()
