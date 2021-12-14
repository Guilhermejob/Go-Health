from flask import jsonify, request, current_app
from app.models.professional_model import ProfessionalModel
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash


def create():
    data = request.get_json()

    session = current_app.db.session

    password_to_hash = data.pop("password")
    professional = ProfessionalModel(**data)
    professional.password = password_to_hash

    session.add(professional)
    session.commit()

    return jsonify(professional), 200


def get_all():

    professional_list = ProfessionalModel.query.all()

    return jsonify(professional_list), 200


def get_by_id(id):
    professional = ProfessionalModel.query.filter_by(id=id).first()
    return jsonify(professional.serialize()), 200


def update():
    
    data = request.get_json()
    
    professional = get_jwt_identity()
    
    if 'password' in data.keys():
        password_to_hash = data.pop('password')
        data['password_hash'] = generate_password_hash(password_to_hash)
    
    ProfessionalModel.query.filter_by(email=professional['email']).update(data)

    current_app.db.session.commit()
    
    if 'password_hash' in data.keys():
        data.pop('password_hash')
        
    return jsonify(data), 200


def delete():
    professional = get_jwt_identity()
    
    ProfessionalModel.query.filter_by(email=professional['email']).delete()
    
    current_app.db.session.commit()
    
    return jsonify({'message': f"Professional {professional['name']} has been deleted."}), 200