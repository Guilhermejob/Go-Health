from flask import jsonify, request, current_app
from app.models.professional_model import ProfessionalModel


def create():
    data = request.get_json()

    session = current_app.db.session

    # send hash to db
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
    professional_list = ProfessionalModel.query.filter_by(id=id).all()
    return jsonify(professional_list), 200
