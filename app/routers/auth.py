from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models, utils, oauth2
from app.database import get_db

router = APIRouter(
    tags=["auth"]
)

@router.post("/login", response_model=schemas.AccessTokenResponse)
async def login(
    login_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Find user by phone number or email
    user = None
    
    # First try to find by phone number
    user = db.query(models.User).filter(
        models.User.phone_number == login_data.username).first()
    
    # If not found by phone, try to find by email
    if not user:
        user = db.query(models.User).filter(
            models.User.email == login_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )

    if not utils.verify_password(login_data.password, str(user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )

    # Create access token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@router.post("/logout")
async def logout(
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """
    Logout endpoint (client should discard the access token)
    """
    return {"message": "Successfully logged out"}
