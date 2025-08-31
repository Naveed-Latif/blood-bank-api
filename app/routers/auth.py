from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models, utils, oauth2
from app.database import get_db
from typing import Optional

router = APIRouter(
    tags=["auth"]
)

@router.post("/login", response_model=schemas.AccessTokenResponse)
async def login(
    response: Response, 
    login_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Find user by phone number
    user = db.query(models.User).filter(
        models.User.phone_number == login_data.username).first()

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

    # Create both access and refresh tokens
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    refresh_token = oauth2.create_refresh_token(user.id, db)
    
    # Set refresh token as HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7*24*60*60,  # 7 days in seconds
        samesite="lax"
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=schemas.AccessTokenResponse)
async def refresh_access_token(
    request: Request,
    refresh_token: Optional[str] = Cookie(None, alias="refresh_token"),
    db: Session = Depends(get_db)
):
    """
    Generate a new access token using a valid refresh token from cookie
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )
    
    try:
        # Verify refresh token
        token_data = oauth2.verify_refresh_token(refresh_token, db)
        
        # Create new access token
        access_token = oauth2.create_access_token(data={"user_id": token_data.id})
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/refresh-json", response_model=schemas.AccessTokenResponse)
async def refresh_access_token_json(
    refresh_request: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a new access token using a valid refresh token from request body
    """
    try:
        # Verify refresh token
        token_data = oauth2.verify_refresh_token(refresh_request.refresh_token, db)
        
        # Create new access token
        access_token = oauth2.create_access_token(data={"user_id": token_data.id})
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout")
async def logout(
    response: Response,
    refresh_token: Optional[str] = Cookie(None, alias="refresh_token"),
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """
    Logout by revoking the refresh token
    """
    try:
        if refresh_token:
            oauth2.revoke_refresh_token(refresh_token, db)
        
        # Clear the refresh token cookie
        response.delete_cookie(key="refresh_token")
        
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error logging out"
        )

@router.post("/logout-json")
async def logout_json(
    refresh_request: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """
    Logout by revoking the refresh token (JSON version)
    """
    try:
        oauth2.revoke_refresh_token(refresh_request.refresh_token, db)
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error logging out"
        )

@router.post("/logout-all")
async def logout_all_devices(
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """
    Logout from all devices by revoking all refresh tokens for the user
    """
    try:
        oauth2.revoke_all_user_tokens(current_user.id, db)
        
        # Clear the refresh token cookie
        response.delete_cookie(key="refresh_token")
        
        return {"message": "Successfully logged out from all devices"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error logging out from all devices"
        )