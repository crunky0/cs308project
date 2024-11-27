import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import database
from fastapi.middleware.cors import CORSMiddleware

from stock_endpoints import router as stock_router  # Import the router
from user_endpoints import router as user_router  # Import the router
from rating_endpoints import router as rating_router
from categorysearch_endpoints import router as category_search_router
from card_endpoints import router as card_router
from invoice_endpoints import router as invoice_router
from product_sort_endpoints import router as product_sort_router
from mailing_endpoints import router as mailing_router
from order_endpoints import router as order_router


# FastAPI app initialization with lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    if not database.is_connected:
        await database.connect()
    yield  # This yields control to the application during its lifespan
    # Shutdown logic
    if database.is_connected:
        await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_router)
app.include_router(user_router)
app.include_router(rating_router)
app.include_router(category_search_router)
app.include_router(card_router)
app.include_router(invoice_router)
app.include_router(product_sort_router)
app.include_router(mailing_router)
app.include_router(order_router)
