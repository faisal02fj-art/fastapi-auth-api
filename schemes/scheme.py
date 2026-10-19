from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Dict, Optional
from typing import Annotated, Literal
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import User


from Services.database import get_db

class createUsers(BaseModel):
    name: Annotated[str, Field(max_length=30, title="Name of User")]
    email: EmailStr
    age: Annotated[int, Field(gt=20, lt=35)]
    password: Annotated[str, Field(min_length= 5, max_length= 8)]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
            valid_doamins = ['gmail.com', 'yahoo.com']
            domain_name = value.split('@')[-1]
    
            if domain_name not in valid_doamins:
                raise ValueError('not in valid doamin')


            return value

# Response Model
class Student(BaseModel):
    id: int
    name: str
    age: int
    email: str
