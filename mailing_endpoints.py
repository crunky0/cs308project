from fastapi import APIRouter, HTTPException
from mailing_service import MailingService  # Importing from the services directory

router = APIRouter()
mailing_service = MailingService()

@router.post("/send_invoice_email")
async def send_invoice_email(recipient_email: str, invoice_file_path: str):
    try:
        response = mailing_service.send_invoice_email(recipient_email, invoice_file_path)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))