from sqlalchemy.orm import Session
from sqlalchemy import extract
from datetime import date, timedelta
from models import Contact, ContactCreate, ContactUpdate


def create_contact(db_session: Session, contact_create: ContactCreate):
    new_contact = Contact(**contact_create.dict())
    db_session.add(new_contact)
    db_session.commit()
    db_session.refresh(new_contact)
    return new_contact


def get_contacts(db_session: Session, skip: int = 0, limit: int = 10):
    return db_session.query(Contact).offset(skip).limit(limit).all()


def get_contact(db_session: Session, contact_id: int):
    return db_session.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db_session: Session, contact_id: int, contact_update: ContactUpdate):
    contact = db_session.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        for field, value in contact_update.dict(exclude_unset=True).items():
            setattr(contact, field, value)
        db_session.commit()
        db_session.refresh(contact)
    return contact


def delete_contact(db_session: Session, contact_id: int):
    contact = db_session.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db_session.delete(contact)
        db_session.commit()
    return contact


def search_contacts(db_session: Session, query: str):
    return db_session.query(Contact).filter(
        (Contact.name.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%")) |
        (Contact.additional_info.ilike(f"%{query}%"))
    ).all()


def get_upcoming_birthdays(db_session: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    return db_session.query(Contact).filter(
        extract('month', Contact.birthday) == today.month,
        extract('day', Contact.birthday) >= today.day,
        extract('day', Contact.birthday) <= next_week.day
    ).all()
