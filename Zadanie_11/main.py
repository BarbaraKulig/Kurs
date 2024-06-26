from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Contact, Base
import crud  # Importujemy moduł crud na początku pliku

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contacts/", response_model=Contact)
def create_new_contact(contact: crud.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, **contact.dict())


@app.get("/contacts/", response_model=list[Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_contacts(db, skip=skip, limit=limit)


@app.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: crud.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id, **contact.dict())
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.delete("/contacts/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.get("/contacts/search/", response_model=list[Contact])
def search_contacts(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return crud.search_contacts(db, query)


@app.get("/contacts/birthdays/", response_model=list[Contact])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return crud.get_upcoming_birthdays(db)
