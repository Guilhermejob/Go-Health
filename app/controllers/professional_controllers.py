from flask import jsonify, request, current_app
from app.models.professional_model import ProfessionalModel
from app.exceptions.professional_exceptions import NotFoundProfessionalError, KeysNotAllowedError, TypeValueError
import sqlalchemy
from app.controllers import format_output_especific_professional, validate_keys_professional, validate_type_value_professional


def create():

    data = request.get_json()

    try:
        validate_keys_professional(data)
        validate_type_value_professional(data)

        session = current_app.db.session

        data['final_rating'] = 0

        # convert password in password_hash
        password_to_hash = data.pop("password")
        professional = ProfessionalModel(**data)
        professional.password = password_to_hash

        session.add(professional)
        session.commit()

        return jsonify(professional), 200

    except sqlalchemy.exc.IntegrityError as err:
        errorInfo = str(err.orig.args)
        msg = errorInfo.split('Key')[1].split('.\\n')[0]
        msg = format_output_especific_professional(msg)
        return jsonify({'error': msg}), 409
    except KeysNotAllowedError as err:
        return jsonify(err.message), 400
    except TypeValueError as err:
        return jsonify(err.message), 400


def get_all():

    professional_list = ProfessionalModel.query.all()

    return jsonify(professional_list), 200


def get_by_id(id):
    try:
        professional = ProfessionalModel.query.filter_by(id=id).first()

        if professional == None:
            raise NotFoundProfessionalError

        return jsonify(professional.serialize()), 200
    except NotFoundProfessionalError as err:
        return jsonify(err.message), 404
