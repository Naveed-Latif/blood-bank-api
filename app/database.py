from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import URL
import os
from dotenv import load_dotenv
from app.config import settings

# Load environment variables
load_dotenv()

# Import settings
# from .config import settings

# Database configuration
DATABASE_URL = URL.create(
    drivername=settings.database_driver_name,
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=settings.database_name,

)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine) 