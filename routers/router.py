"""Routes: receive the request, call the service, return the response."""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordRequestForm, OAuth2PasswordBearer


from schemes.scheme import createUsers, Student
from models.models import User
from Services.database import get_db
from Services.auth import hash_password, verify_password, create_token, verify_token



router = APIRouter()

# Register
@router.post("/register", response_model=Student)
def register_user(user: createUsers, db:Session = Depends(get_db)):

        # 1) NEW: check first, before creating anything
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    
    new_user = User(
        name = user.name,
        email = user.email,
        password=hash_password(user.password),
        age = user.age
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{
        "message":"User Register Successfully",
        "id": new_user.id,
        "name" : new_user.name,
        "email" :new_user.email,
        "password" : new_user.password,
        "age":  new_user.age
    }

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),
        db:Session=Depends(get_db)
    ):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):  # (4) compare
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_token({
        "sub": form_data.username
    })
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# Protected Route
@router.get("/Secure")
def secure_data(username:str=Depends(verify_token)):

    return {
        "message": "Secure data access",
        "user": username
    }