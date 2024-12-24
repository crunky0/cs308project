import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import database
from fastapi.middleware.cors import CORSMiddleware
from product_manager_endpoints import manager_router
from user_endpoints import router as user_router  # Import the router
from rating_endpoints import router as rating_router
from categorysearch_endpoints import router as category_search_router
from delivery_endpoints import router as delivery_router
from invoice_endpoints import router as invoice_router
from order_endpoints import router as order_router
from product_endpoints import router as product_router

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

app.include_router(manager_router)
app.include_router(user_router)
app.include_router(rating_router)
app.include_router(category_search_router)
app.include_router(invoice_router)
app.include_router(order_router)
app.include_router(delivery_router)
app.include_router(product_router)