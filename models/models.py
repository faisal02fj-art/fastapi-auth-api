import os
from fastapi import Depends
from sqlalchemy.orm import  Session
from sqlalchemy import Column, Integer, String
from Services.database import base
from Services.database import get_db

class User(base):
    __tablename__ = "users_info"

    id = Column(Integer, primary_key=True,  index=True)
    name = Column(String(100),nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False, )
    age = Column(Integer, nullable=False)


