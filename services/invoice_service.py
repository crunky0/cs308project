import os
import pdfkit
from datetime import datetime
import logging
from typing import List, Dict, Any
import platform

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if platform.system() == "Windows":
    path_wkhtmltopdf = 'D:\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
else:
    path_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'  # Path for macOS/Linux

pdfkit_config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

class InvoiceService:
    def __init__(self, output_dir: str = "invoices"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        logger.info(f"Invoice output directory set to: {self.output_dir}")

    def generate_invoice(
        self, user_info: Dict[str, str], items: List[Dict[str, Any]], total_amount: float
    ) -> str:
        try:
            # Validate input data
            self._validate_input_data(user_info, items, total_amount)

            # Generate unique invoice number and date
            invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            invoice_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Generate the HTML content for the invoice
            html_content = self._create_invoice_html(
                invoice_number, invoice_date, user_info, items, total_amount
            )

            # Save HTML content to file for debugging
            html_file_path = os.path.join(self.output_dir, f"{invoice_number}.html")
            with open(html_file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.debug(f"Invoice HTML saved at: {html_file_path}")

            # Define file path for the PDF
            file_path = os.path.join(self.output_dir, f"{invoice_number}.pdf")

            # Generate PDF from HTML
            pdfkit.from_string(html_content, file_path, configuration=pdfkit_config)
            logger.info(f"Invoice generated successfully: {file_path}")

            return file_path

        except Exception as e:
            logger.error("Error generating invoice.", exc_info=True)
            raise Exception("Failed to generate invoice") from e

    def _validate_input_data(
        self, user_info: Dict[str, str], items: List[Dict[str, Any]], total_amount: float
    ):
        if not user_info.get('name') or not user_info.get('email'):
            raise ValueError("User name or email is missing.")
        for item in items:
            if not item.get('name'):
                raise ValueError("An item is missing a name.")
            if not isinstance(item.get('quantity'), int):
                raise ValueError("Item quantity must be an integer.")
            if not isinstance(item.get('price'), (int, float)):
                raise ValueError("Item price must be a number.")

    def _create_invoice_html(
        self, invoice_number: str, invoice_date: str, user_info: Dict[str, str],
        items: List[Dict[str, Any]], total_amount: float
    ) -> str:
        # Simplified HTML template for testing
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Invoice {invoice_number}</title>
        </head>
        <body>
            <h1>Invoice {invoice_number}</h1>
            <p>Date: {invoice_date}</p>
            <p>Customer: {user_info.get('name')}</p>
            <p>Email: {user_info.get('email')}</p>
            <h2>Items:</h2>
            <ul>
                {''.join([f"<li>{item['name']} - Quantity: {item['quantity']}, Price: ${item['price']}</li>" for item in items])}
            </ul>
            <p>Total Amount: ${total_amount:.2f}</p>
        </body>
        </html>
        """
        return html_template
