from fastapi import APIRouter, Depends, HTTPException, status,Response,Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models, utils, oauth2
from app.database import get_db
from typing import Optional

router = APIRouter(
    tags=["auth"]
)
@router.post("/login", response_model=schemas.Token)
async def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Find user by phone number
    user = db.query(models.User).filter(
        models.User.phone_number == login_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not utils.verify_password(login_data.password, str(user.password)):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    refresh_token = oauth2.create_refresh_token(user.id, db)
        
        # Set refresh token as HTTP-only cookie
    Response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=7*24*60*60,  # 7 days in seconds
            samesite="lax"
        )
    return {"access_token": access_token, "token_type": "bearer"}