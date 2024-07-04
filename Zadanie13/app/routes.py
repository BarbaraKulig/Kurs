from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .schemas import UserCreate, UserUpdate, ContactCreate
from .models import User, Contact
from .services import get_user_by_email, create_user, update_avatar, send_verification_email, verify_email_token, \
    create_contact, get_contacts_count
from .database import get_db
from fastapi_limiter.depends import RateLimiter
import cloudinary.uploader

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db=db, user=user)
    send_verification_email(new_user.email)
    return new_user


@router.post("/update-avatar", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def update_user_avatar(user_id: int, avatar_url: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    result = cloudinary.uploader.upload(avatar_url)
    update_avatar(db=db, user_id=user_id, avatar_url=result['url'])
    return {"msg": "Avatar updated successfully"}


@router.post("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    db.commit()
    return {"msg": "Email verified successfully"}


@router.post("/contacts", dependencies=[Depends(RateLimiter(times=settings.rate_limit, seconds=60))])
def create_new_contact(contact: ContactCreate, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    contacts_count = get_contacts_count(db=db, user_id=user_id)
    if contacts_count >= settings.rate_limit:
        raise HTTPException(status_code=400, detail="Contact limit reached")
    return create_contact(db=db, contact=contact, user_id=user_id)
