# app/contact.py

class Contact:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class ContactManager:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def get_contacts(self):
        return self.contacts
