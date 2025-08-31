from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "6a2b9312bc078929af5193e56f966e1e6f0c309c13b7462eb413b2c1bf2d4aac"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: str, db: Session):
    # Import here to avoid circular imports
    from app import models
    
    # Create refresh token data
    to_encode = {
        "user_id": user_id,
        "type": "refresh",
        "exp": datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    }
    
    # Encode the JWT
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Store in database
    token_id = str(uuid.uuid4())
    db_refresh_token = models.RefreshToken(
        id=token_id,
        user_id=user_id,
        token=refresh_token,
        expires_at=datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    # Deactivate old refresh tokens for this user (optional - you can keep multiple active)
    db.query(models.RefreshToken).filter(
        models.RefreshToken.user_id == user_id,
        models.RefreshToken.is_active == True
    ).update({"is_active": False})
    
    db.add(db_refresh_token)
    db.commit()
    
    return refresh_token

def verify_token(token: str, credentials_exception, token_type: str = "access"):
    # Import here to avoid circular imports
    from app import schemas
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        token_type_payload = payload.get("type")
        
        if user_id is None or token_type_payload != token_type:
            raise credentials_exception
            
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data

def verify_refresh_token(refresh_token: str, db: Session):
    # Import here to avoid circular imports
    from app import models
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify JWT structure and signature
    token_data = verify_token(refresh_token, credentials_exception, "refresh")
    
    # Check if token exists in database and is active
    db_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == refresh_token,
        models.RefreshToken.is_active == True,
        models.RefreshToken.expires_at > datetime.now()
    ).first()
    
    if not db_token:
        raise credentials_exception
    
    return token_data

def revoke_refresh_token(refresh_token: str, db: Session):
    """Revoke a specific refresh token"""
    from app import models
    
    db.query(models.RefreshToken).filter(
        models.RefreshToken.token == refresh_token
    ).update({"is_active": False})
    db.commit()

def revoke_all_user_tokens(user_id: str, db: Session):
    """Revoke all refresh tokens for a user"""
    from app import models
    
    db.query(models.RefreshToken).filter(
        models.RefreshToken.user_id == user_id,
        models.RefreshToken.is_active == True
    ).update({"is_active": False})
    db.commit()

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user token data only"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)