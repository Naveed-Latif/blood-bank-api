from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import URL
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from app.config import settings

# Load environment variables
load_dotenv()

# Import settings
# from .config import settings

# Database configuration - URL.create handles special characters automatically
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",  # Specify the driver explicitly
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=int(settings.database_port),
    database=settings.database_name,
    query={"sslmode": "require"}  # Supabase requires SSL
)

# Create SQLAlchemy engine with SSL parameters
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    """Get database session with error handling for connection failures."""
    db = SessionLocal()
    try:
        # Test the connection by executing a simple query
        # This will raise OperationalError if the database is unavailable
        db.execute(text("SELECT 1"))
        yield db
    except OperationalError as e:
        # Database connection failed - return 503 Service Unavailable
        db.close()
        raise HTTPException(
            status_code=503,  # HTTP_503_SERVICE_UNAVAILABLE
            detail="Database service is currently unavailable. Please try again later."
        )
    except Exception as e:
        # Other database errors
        db.close()
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=503,  # HTTP_503_SERVICE_UNAVAILABLE
            detail="Database service error. Please try again later."
        )
    finally:
        db.close()

# Create all tables
def create_tables():
    """Create all database tables. Handles connection errors gracefully."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        # Log the error but don't crash the application
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to create tables during startup: {e}")
        logger.info("Tables will be created automatically on first database connection") 