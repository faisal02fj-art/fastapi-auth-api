
from fastapi import APIRouter


router = APIRouter()

@router.get("/")
def Home():
    return{
        "message": "Welcome to My auth api"
    }
