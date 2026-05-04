from sqlalchemy import Column, String, Date, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=True, index=True)
    phone_number = Column(String(15), unique=True, nullable=False, index=True)
    blood_group = Column(String(3), nullable=False)
    last_donation_date = Column(Date, nullable=True)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)  # In production, this should be hashed
    registration_date = Column(TIMESTAMP(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, phone={self.phone_number})>"