import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Dict, Any

class MailingService:
    def send_invoice_email(self, recipient_email: str, invoice_file_path: str) -> Dict[str, str]:
        try:
            # Ensure the invoice file exists
            if not os.path.exists(invoice_file_path):
                raise FileNotFoundError(f"The invoice file '{invoice_file_path}' does not exist.")

            # Load email credentials from environment variables
            from_email = os.getenv('EMAIL_MAIL_USERNAME')  # Sender email address (e.g., Gmail, Outlook)
            password = os.getenv('EMAIL_MAIL_PASSWORD')   # Email password or App password

            # Check if credentials are provided
            if not from_email or not password:
                raise ValueError("Email credentials are not set correctly. Please check your environment variables.")

            # Email message configuration
            message = MIMEMultipart()
            message['From'] = from_email
            message['To'] = recipient_email
            message['Subject'] = "Your Invoice"

            # Attach body text (you can customize this text)
            body = "Dear customer, \n\nPlease find attached your invoice. \n\nBest regards, Your Company"
            message.attach(MIMEText(body, 'plain'))

            # Attach the PDF invoice
            with open(invoice_file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(invoice_file_path)}"')
                message.attach(part)

            # Connect to SMTP server and send email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Using SMTP Gmail server (change if needed)
                server.starttls()  # Start TLS (secure connection)
                server.login(from_email, password)  # Login to the email server
                server.send_message(message)  # Send the email

            return {"message": "Invoice email sent successfully"}

        except FileNotFoundError as fnf_error:
            raise Exception(f"File error: {fnf_error}")
        except smtplib.SMTPAuthenticationError:
            raise Exception("Authentication failed. Please check your email credentials.")
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
