from crewai.tools import BaseTool
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class EmailSMTPTool(BaseTool):
    name: str = "Gmail SMTP Sender"
    description: str = "Sends an email using Gmail SMTP. Input format: recipient | subject | message body"

    def _run(self, input_text: str) -> str:
        try:
            parts = input_text.split("|")
            if len(parts) != 3:
                return "❌ Invalid format. Use: recipient | subject | message"

            recipient, subject, message = [p.strip() for p in parts]

            gmail_user = os.getenv("GMAIL_USER")
            gmail_pass = os.getenv("GMAIL_PASS")

            msg = MIMEText(message,"html","utf-8")
            msg["Subject"] = subject
            msg["From"] = gmail_user
            msg["To"] = recipient

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(gmail_user, gmail_pass)
                server.sendmail(gmail_user, recipient, msg.as_string())

            return f"✅ Email sent to {recipient} with subject '{subject}'"

        except Exception as e:
            return f"❌ Error sending email: {str(e)}"
