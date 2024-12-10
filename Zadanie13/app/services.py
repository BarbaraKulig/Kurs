from sqlalchemy.orm import Session
from .models import User, Contact
from .schemas import UserCreate, ContactCreate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jose import JWTError, jwt
from .config import settings
from datetime import datetime, timedelta


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_avatar(db: Session, user_id: int, avatar_url: str):
    user = db.query(User).filter(User.id == user_id).first()
    user.avatar_url = avatar_url
    db.commit()
    db.refresh(user)
    return user


def send_verification_email(email: str):
    token = create_verification_token(email)
    msg = MIMEMultipart()
    msg['From'] = "your_email@example.com"
    msg['To'] = email
    msg['Subject'] = "Email Verification"
    body = f"Please verify your email using the following token: {token}"
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login("your_email@example.com", "your_password")
        text = msg.as_string()
        server.sendmail(msg['From'], msg['To'], text)


def create_verification_token(email: str):
    to_encode = {"email": email, "exp": datetime.utcnow() + timedelta(hours=1)}
    encoded_jwt = jwt.encode(to_encode, settings.email_verification_secret, algorithm="HS256")
    return encoded_jwt


def verify_email_token(token: str):
    try:
        payload = jwt.decode(token, settings.email_verification_secret, algorithms=["HS256"])
        email = payload.get("email")
        if email is None:
            raise JWTError()
        return email
    except JWTError:
        return None


def create_contact(db: Session, contact: ContactCreate, user_id: int):
    db_contact = Contact(**contact.dict(), user_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts_count(db: Session, user_id: int):
    return db.query(Contact).filter(Contact.user_id == user_id).count()
