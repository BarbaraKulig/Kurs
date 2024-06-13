from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Contact
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    current_user_id = get_jwt_identity()
    contacts = Contact.query.filter_by(user_id=current_user_id).all()
    return jsonify([contact.serialize() for contact in contacts]), 200

@main_bp.route('/contacts/<int:contact_id>', methods=['GET'])
@jwt_required()
def get_contact(contact_id):
    current_user_id = get_jwt_identity()
    contact = Contact.query.filter_by(id=contact_id, user_id=current_user_id).first()
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404
    return jsonify(contact.serialize()), 200

@main_bp.route('/contacts', methods=['POST'])
@jwt_required()
def create_contact():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    new_contact = Contact(name=data['name'], email=data['email'], user_id=current_user_id)
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'message': 'Contact created successfully'}), 201

@main_bp.route('/contacts/<int:contact_id>', methods=['PUT'])
@jwt_required()
def update_contact(contact_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    contact = Contact.query.filter_by(id=contact_id, user_id=current_user_id).first()
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404
    contact.name = data['name']
    contact.email = data['email']
    db.session.commit()
    return jsonify({'message': 'Contact updated successfully'}), 200

@main_bp.route('/contacts/<int:contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
    current_user_id = get_jwt_identity()
    contact = Contact.query.filter_by(id=contact_id, user_id=current_user_id).first()
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted successfully'}), 200
