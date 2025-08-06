from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from db.models import User, get_db
from schemas.users import (
    GoogleTokenRequest, 
    TokenResponse, 
    UserResponse, 
    UserCreate
)
from utils.auth import (
    verify_google_token, 
    create_access_token, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/google-signin", response_model=TokenResponse)
async def google_signin(
    token_request: GoogleTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Sign in with Google OAuth token
    """
    # Verify Google token and get user info
    google_user_info = verify_google_token(token_request.token)
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        User.google_id == google_user_info['google_id']
    ).first()
    
    if existing_user:
        # User exists, update their information if needed
        existing_user.name = google_user_info['name']
        existing_user.profile_picture = google_user_info.get('profile_picture')
        db.commit()
        db.refresh(existing_user)
        user = existing_user
    else:
        # Create new user
        user_data = UserCreate(
            email=google_user_info['email'],
            name=google_user_info['name'],
            google_id=google_user_info['google_id'],
            profile_picture=google_user_info.get('profile_picture')
        )
        
        user = User(**user_data.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get current user's profile information
    Requires authentication via Bearer token
    """
    return current_user

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Alternative endpoint to get current user information
    Requires authentication via Bearer token
    """
    return current_user