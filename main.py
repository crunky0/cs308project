import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI app initialization
app = FastAPI()

# Pydantic models for request bodies
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Load SQL from file function
def load_sql_file(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()

# Helper functions for password handling
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Connect to the database when the app starts
@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

# Disconnect from the database when the app shuts down
@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

# API Endpoint to create a new user
@app.post("/users/register/")
async def create_user(user: UserCreate):
    # Load the SQL query from the file
    sql_query = load_sql_file('sql/create_user.sql')

    # Check if the username already exists
    find_user_query = load_sql_file('sql/find_user_by_username.sql')
    existing_user = await database.fetch_one(query=find_user_query, values={"username": user.username})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password and execute the SQL file to insert the new user
    hashed_password = hash_password(user.password)
    values = {"username": user.username, "password": hashed_password, "role": "Customer"}
    await database.execute(query=sql_query, values=values)
    
    return {"message": "User created successfully"}

# API Endpoint to login
@app.post("/users/login/")
async def login(user: UserLogin):
    # Load the SQL query from the file
    sql_query = load_sql_file('sql/find_user_by_username.sql')

    # Fetch the user by username
    db_user = await database.fetch_one(query=sql_query, values={"username": user.username})

    # Check if user exists and password matches
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful", "user": db_user["username"]}
