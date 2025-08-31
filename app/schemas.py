from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional
import re

# Request schemas
class SignupRequest(BaseModel):
    name: str
    last_name: str
    phone_number: str
    blood_group: str
    last_donation_date: Optional[date] = None
    city: str
    country: str
    password: str

    @field_validator("name", "last_name")
    @classmethod
    def validate_names(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name should only contain letters and spaces")
        return v.strip()

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        digits_only = re.sub(r"\D", "", v)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError("Phone number should be between 10-15 digits")
        return digits_only

    @field_validator("blood_group")
    @classmethod
    def validate_blood_group(cls, v):
        valid_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        if v.upper() not in valid_groups:
            raise ValueError(f"Blood group must be one of: {', '.join(valid_groups)}")
        return v.upper()

    @field_validator("last_donation_date")
    @classmethod
    def validate_donation_date(cls, v):
        if v and v > date.today():
            raise ValueError("Last donation date cannot be in the future")
        return v

    @field_validator("country")
    @classmethod
    def validate_country(cls, v):
        if v.strip().lower() != "pakistan":
            raise ValueError("Currently, only registrations from Pakistan are accepted.")
        return v.strip().title()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not (8 <= len(v) <= 20):
            raise ValueError("Password must be between 8 and 20 characters long.")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for c in v):
            raise ValueError("Password must contain at least one special character.")
        return v

class LoginRequest(BaseModel):
    phone_number: str
    password: str

# Response schemas
class SignupResponse(BaseModel):
    name: str
    last_name: str
    phone_number: str
    blood_group: str
    last_donation_date: Optional[date]
    city: str
    country: str
    message: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    name: str
    last_name: str
    phone_number: str
    blood_group: str
    last_donation_date: Optional[date]
    city: str
    country: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None