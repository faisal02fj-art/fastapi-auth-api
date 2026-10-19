from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine
from fastapi import Depends

from Services.config import setting
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = setting.db_url

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Session_local = sessionmaker(
    bind= engine,
    autoflush = False,
    autocommit = False
)

base = declarative_base()


def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()

