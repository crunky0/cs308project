from fastapi import FastAPI, HTTPException,APIRouter
from pydantic import BaseModel
from databases import Database
from passlib.context import CryptContext
from db import database

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create APIRouter instance for user-related endpoints
router = APIRouter()

# Pydantic models for request bodies
class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    email: str
    taxID: str
    homeAddress: str

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

#API endpoint to create a user
@router.post("/users/register/")
async def create_user(user: UserCreate):
    # Load the SQL query from the file
    sql_query = load_sql_file('sql/create_user.sql')

    # Check if the username or email already exists
    find_user_query = "SELECT * FROM users WHERE username = :username OR email = :email"
    existing_user = await database.fetch_one(query=find_user_query, values={"username": user.username, "email": user.email})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Hash the password and insert the new user
    hashed_password = hash_password(user.password)
    values = {
        "username": user.username,
        "password": hashed_password,
        "role": "Customer",
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "taxid": user.taxID,
        "homeaddress": user.homeAddress
    }
    db_user = await database.fetch_one(query=sql_query, values=values)
    
    return {
        "message": "Signup successful",
        "user": {
            "userid": db_user["userid"],
            "email": user.email
        }
    }


# API Endpoint to login
@router.post("/users/login/")
async def login(user: UserLogin):
    # Load the SQL query from the file
    sql_query = load_sql_file('sql/find_user_by_username.sql')

    # Fetch the user by username
    db_user = await database.fetch_one(query=sql_query, values={"username": user.username})

    # Check if user exists and password matches
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Return userID and username
    return {
        "message": "Login successful",
        "user": {
            "userid": db_user["userid"],  
            "email": db_user["username"]
        }
    }