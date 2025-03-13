# tools/email_delivery_tool.py
from langchain.tools import BaseTool
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

class EmailDeliveryTool(BaseTool):
    name: str = "Email Delivery"
    description: str = "Useful for sending medical reports via email."

    def _run(self, input_str: str) -> str:
        """Use the tool."""
        try:
            to_email, subject, body = input_str.split("|||") #to_email|||subject|||body
            from_email = os.getenv("EMAIL_FROM")
            password = os.getenv("EMAIL_PASSWORD")
            smtp_server = os.getenv("SMTP_SERVER")
            smtp_port = int(os.getenv("SMTP_PORT"))

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = from_email
            msg["To"] = to_email

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(from_email, password)
                server.sendmail(from_email, to_email, msg.as_string())
            return "Email sent successfully."
        except Exception as e:
            return f"Error sending email: {e}"

    def _arun(self, input_str: str):
        """Use the tool asynchronously."""
        raise NotImplementedError("This tool does not support async")