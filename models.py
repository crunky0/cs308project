from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    # Define the columns with the appropriate data types
    userid = Column(Integer, primary_key=True, autoincrement=True)  # Auto-incrementing ID (serial4)
    username = Column(String(50), unique=True, index=True)  # Username column (varchar(100))
    password = Column(String(255))  # Password column (varchar(255))
    role = Column(String(50))  # Role column (varchar(50))
    name = Column(String(100))  # Name column (varchar(100))
    surname = Column(String(100))  # Surname column (varchar(100))
    email = Column(String(100), unique=True)  # Email column (varchar(100), unique)
    taxid = Column(String(50))  # Tax ID column (varchar(50))
    homeaddress = Column(String(255))  # Home address column (varchar(255))
