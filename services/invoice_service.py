import os
import pdfkit
from datetime import datetime
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class InvoiceService:
    def __init__(self, output_dir: str = "invoices"):
        """
        Initialize the InvoiceService with an output directory.
        """
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        logger.info(f"Invoice output directory set to: {self.output_dir}")

        # Configure wkhtmltopdf path
        self.pdfkit_config = pdfkit.configuration(wkhtmltopdf=r"D:\wkhtmltopdf\bin\wkhtmltopdf.exe")

    def generate_invoice(self, html_content: str, invoice_number: str) -> str:
        """
        Generate the PDF invoice from the given HTML content.
        """
        try:
            file_path = os.path.join(self.output_dir, f"{invoice_number}.pdf")
            pdfkit.from_string(html_content, file_path, configuration=self.pdfkit_config)
            logger.info(f"Invoice PDF generated successfully: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error generating invoice: {e}", exc_info=True)
            raise Exception("Failed to generate invoice.") from e

    def _create_invoice_html(
        self, invoice_number: str, invoice_date: str, user_info: Dict[str, str],
        items: List[Dict[str, Any]], total_amount: float
    ) -> str:
        """
            Creates a clean and minimalistic HTML template for the invoice.
        """
        css_styles = """
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f9f9f9;
            }
            .invoice-container {
                margin: 40px auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #ffffff;
                max-width: 700px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .invoice-header {
                text-align: center;
                margin-bottom: 20px;
            }
            .invoice-header h1 {
                font-size: 28px;
                color: #333;
                margin: 0;
            }
            .invoice-details {
                margin-bottom: 30px;
            }
            .invoice-details p {
                margin: 5px 0;
                color: #555;
            }
            .invoice-items {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }
            .invoice-items th, .invoice-items td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }
            .invoice-items th {
                background-color: #f2f2f2;
                color: #333;
            }
            .invoice-summary {
                text-align: right;
            }
            .invoice-summary p {
                margin: 5px 0;
                color: #333;
                font-size: 16px;
                font-weight: bold;
            }
            .footer {
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #999;
            }
        </style>
        """

        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Invoice {invoice_number}</title>
            {css_styles}
        </head>
        <body>
            <div class="invoice-container">
                <!-- Invoice Header -->
                <div class="invoice-header">
                    <h1>INVOICE</h1>
                </div>

                <!-- Invoice Details -->
                <div class="invoice-details">
                    <p><strong>Invoice Number:</strong> {invoice_number}</p>
                    <p><strong>Invoice Date:</strong> {invoice_date}</p>
                    <p><strong>Customer Name:</strong> {user_info.get('name')}</p>
                    <p><strong>Customer Email:</strong> {user_info.get('email')}</p>
                </div>

                <!-- Items Table -->
                <table class="invoice-items">
                    <thead>
                        <tr>
                            <th>Item Name</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join([f"<tr><td>{item['name']}</td><td>{item['quantity']}</td><td>${item['price']:.2f}</td><td>${item['quantity'] * item['price']:.2f}</td></tr>" for item in items])}
                    </tbody>
                </table>

                <!-- Summary -->
                <div class="invoice-summary">
                    <p><strong>Total Amount:</strong> ${total_amount:.2f}</p>
                </div>

                <!-- Footer -->
                <div class="footer">
                    <p>Thank you for your business!</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_template
