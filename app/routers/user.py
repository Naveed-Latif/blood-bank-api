from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, utils
from app.database import get_db
from app.oauth2 import get_current_user
from app import oauth2

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
# Get all registered users  
@router.get("/", response_model=list[schemas.UserResponse])
async def get_users(db: Session = Depends(get_db), id = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users


# Get users by blood group
@router.get("/blood-group/{blood_group}", response_model=list[schemas.UserResponse])
async def get_users_by_blood_group(blood_group: str, db: Session = Depends(get_db), id = Depends(oauth2.get_current_user)):
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
async def get_user(user_id: str, db: Session = Depends(get_db), id = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

