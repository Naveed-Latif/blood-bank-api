from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, utils
from app.database import get_db
from app import oauth2

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

def get_current_user_from_db(
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user)
):
    """Get current user object from database"""
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

# Get all registered users  
@router.get("/", response_model=list[schemas.UserResponse])
async def get_users(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user_from_db)
):
    users = db.query(models.User).all()
    return users

# Get users by blood group
@router.get("/blood-group/{blood_group}", response_model=list[schemas.UserResponse])
async def get_users_by_blood_group(
    blood_group: str, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user_from_db)
):
    # Validate blood group
    valid_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    if blood_group.upper() not in valid_groups:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid blood group. Must be one of: {', '.join(valid_groups)}"
        )
    
    # Search users by blood group
    users = db.query(models.User).filter(
        models.User.blood_group == blood_group.upper()
    ).all()
    
    if not users:
        raise HTTPException(
            status_code=404, 
            detail=f"No users found with blood group {blood_group.upper()}"
        )
    
    return users

# Get specific user by ID (keeping for admin purposes)
@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(
    user_id: str, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user_from_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get current user's profile
@router.get("/me/profile", response_model=schemas.UserResponse)
async def get_my_profile(
    current_user: models.User = Depends(get_current_user_from_db)
):
    """Get the current user's profile"""
    return current_user