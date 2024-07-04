# tests/test_contact.py

import pytest
from app.contact import Contact, ContactManager

def test_create_contact():
    contact = Contact(name="John Doe", email="john.doe@example.com")
    assert contact.name == "John Doe"
    assert contact.email == "john.doe@example.com"

def test_add_contact():
    contact_manager = ContactManager()
    contact = Contact(name="John Doe", email="john.doe@example.com")
    contact_manager.add_contact(contact)
    assert len(contact_manager.get_contacts()) == 1
    assert contact_manager.get_contacts()[0].name == "John Doe"
    assert contact_manager.get_contacts()[0].email == "john.doe@example.com"

def test_get_contacts():
    contact_manager = ContactManager()
    contact1 = Contact(name="John Doe", email="john.doe@example.com")
    contact2 = Contact(name="Jane Doe", email="jane.doe@example.com")
    contact_manager.add_contact(contact1)
    contact_manager.add_contact(contact2)
    contacts = contact_manager.get_contacts()
    assert len(contacts) == 2
    assert contacts[0].name == "John Doe"
    assert contacts[0].email == "john.doe@example.com"
    assert contacts[1].name == "Jane Doe"
    assert contacts[1].email == "jane.doe@example.com"
