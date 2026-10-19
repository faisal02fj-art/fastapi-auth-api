import os
from fastapi import FastAPI, Depends, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import json

from Services.database import get_db
from Services.config import setting

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
    #oauth ssetup
oath_setup = OAuth2PasswordBearer(os.getenv("TOKEN_URL"))

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)

def create_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=int(setting.access_token_exp_time))

    to_encode.update(
        {"exp": expire}
    )

    token = jwt.encode(
        to_encode,
        setting.secret_kay,
        algorithm=setting.algorithem
    )

    return token


def verify_token(token:str=Depends(oath_setup)):
    try:
        payload = jwt.decode(
            token,
            setting.secret_kay,
            algorithms=setting.algorithem
        )

        username:str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized Token"
            )

        return username
    
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


