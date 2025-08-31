from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, utils
from app.database import get_db
import uuid

router = APIRouter(
    prefix="/signup",
    tags=["signup"]
)


@router.post("/", response_model=schemas.SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: schemas.SignupRequest, db: Session = Depends(get_db)):
    # Check if phone number already exists
    existing_user = db.query(models.User).filter(
        models.User.phone_number == user_data.phone_number).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Phone number already registered")

    # Generate unique user ID
    user_id = f"USER_{uuid.uuid4().hex[:8].upper()}"

    # Create user record
    user_dict = user_data.model_dump(exclude={"confirm_password"})
    raw_password = user_dict.pop("password")
    hashed_password = utils.hash_password(raw_password)
    db_user = models.User(**user_dict, id=user_id, password=hashed_password)

    # Add to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Return response with message field (fix: avoid duplicate 'message')
    data = schemas.SignupResponse.model_validate(db_user).model_dump()
    data["message"] = "Registration successful! Thank you for signing up for blood donation."
    return schemas.SignupResponse(**data)