
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Now your FastAPI setup
from fastapi import FastAPI
from mailing_endpoints import router as mailing_router

app = FastAPI()
app.include_router(mailing_router, prefix="/mailing", tags=["Mailing Service"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Invoice Mailing Service!"}
