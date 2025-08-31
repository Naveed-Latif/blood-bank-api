# import os
# from sqlalchemy.engine import URL
# from typing import Optional

# class Settings:
#     # Database settings
#     DATABASE_URL: str = os.getenv(
#         "DATABASE_URL",
#         "sqlite:///./blood_donation.db"
#     )
    
#     # API settings
#     API_V1_STR: str = "/api/v1"
#     PROJECT_NAME: str = "Blood Donation API"
    
#     # Security settings (for production)
#     SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# settings = Settings() 