import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


SQLALCHEMY_SCHEMA = os.getenv("SQLALCHEMY_SCHEMA", "postgresql+pg8000")
DB_USER = os.getenv("DB_USER", "user")
DB_HOST = os.getenv("DB_HOST", "host")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME", "name")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

SQLALCHEMY_DATABASE_URL = f"{SQLALCHEMY_SCHEMA}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
