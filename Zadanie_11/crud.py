# crud.py

from sqlalchemy.orm import Session
from models import Contact

def create_contact(db_session: Session, name: str, email: str, phone_number: str, birthday: date, additional_info: str = None):
    new_contact = Contact(name=name, email=email, phone_number=phone_number, birthday=birthday, additional_info=additional_info)
    db_session.add(new_contact)
    db_session.commit()
    db_session.refresh(new_contact)
    return new_contact

def get_contacts(db_session: Session, skip: int = 0, limit: int = 10):
    return db_session.query(Contact).offset(skip).limit(limit).all()

def get_contact(db_session: Session, contact_id: int):
    return db_session.query(Contact).filter(Contact.id == contact_id).first()

def update_contact(db_session: Session, contact_id: int, name: str, email: str, phone_number: str, birthday: date, additional_info: str = None):
    contact = db_session.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = name
        contact.email = email
        contact.phone_number = phone_number
        contact.birthday = birthday
        contact.additional_info = additional_info
        db_session.commit()
        db_session.refresh(contact)
    return contact

def delete_contact(db_session: Session, contact_id: int):
    contact = db_session.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db_session.delete(contact)
        db_session.commit()
    return contact
