import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Dict

class MailingService:
    def send_email(self, recipient_email: str, subject: str, body: str) -> None:
        try:
            # Load email credentials from environment variables
            from_email = os.getenv('EMAIL_MAIL_USERNAME')
            password = os.getenv('EMAIL_MAIL_PASSWORD')

            if not from_email or not password:
                raise ValueError("Email credentials are not set correctly.")

            # Create the email message
            message = MIMEMultipart()
            message["From"] = from_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "html"))

            # Connect to SMTP server and send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(from_email, password)
                server.send_message(message)
        except Exception as e:
            raise Exception(f"Failed to send email to {recipient_email}: {str(e)}")
    def send_invoice_email(self, recipient_email: str, invoice_file_path: str) -> Dict[str, str]:
        """
        Sends a formal email with the invoice attached as a PDF.
        """
        try:
            # Ensure the invoice file exists
            if not os.path.exists(invoice_file_path):
                raise FileNotFoundError(f"The invoice file '{invoice_file_path}' does not exist.")

            # Load email credentials from environment variables
            from_email = os.getenv('EMAIL_MAIL_USERNAME')  # Sender email address
            password = os.getenv('EMAIL_MAIL_PASSWORD')   # Email password or App password

            # Check if credentials are provided
            if not from_email or not password:
                raise ValueError("Email credentials are not set correctly. Please check your environment variables.")

            # Create the email message
            message = MIMEMultipart()
            message['From'] = from_email
            message['To'] = recipient_email
            message['Subject'] = "Invoice for Your Recent Purchase"

            # Formal email body with HTML content
            body = f"""
            <html>
            <body>
                <p>Dear Customer,</p>
                <p>Thank you for your recent purchase! Please find attached the invoice for your records.</p>
                <p>If you have any questions or concerns, feel free to contact us at cs308project@example.com.</p>
                <br>
                <p>Best regards,</p>
                <p><strong>CS308 Company </strong></p>
                <p><i>Providing excellent service is our priority.</i></p>
            </body>
            </html>
            """
            message.attach(MIMEText(body, 'html'))  # Attach the body as HTML

            # Attach the PDF invoice
            with open(invoice_file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{os.path.basename(invoice_file_path)}"'
                )
                message.attach(part)

            # Connect to SMTP server and send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Using Gmail's SMTP server (adjust if needed)
                server.starttls()  # Start TLS for secure connection
                server.login(from_email, password)  # Login to the email server
                server.send_message(message)  # Send the email

            return {"message": "Invoice email sent successfully"}

        except FileNotFoundError as fnf_error:
            raise Exception(f"File error: {fnf_error}")
        except smtplib.SMTPAuthenticationError:
            raise Exception("Authentication failed. Please check your email credentials.")
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
