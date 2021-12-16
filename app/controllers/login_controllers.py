from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.exceptions.login_exceptions import EmailNotFoundError, IncorrectPasswordError, InvalidKeyError
from app.models.client_model import ClientModel
from app.models.professional_model import ProfessionalModel


@jwt_required()
def get_user_info():
    user = get_jwt_identity()
    return jsonify(user), 200


def signin_client():

    data = request.get_json()

    try:
        if len(data) > 2 or not 'email' in data.keys() or not 'password' in data.keys():
            raise InvalidKeyError(data)

        client = ClientModel.query.filter_by(email=data['email']).first()

        if not client:
            raise EmailNotFoundError(data['email'])

        if not client.check_password(data['password']):
            raise IncorrectPasswordError()

        access_token = create_access_token(client)

    except EmailNotFoundError as error:
        return jsonify(error.message), 404
    except IncorrectPasswordError as error:
        return jsonify(error.message), 401
    except InvalidKeyError as error:
        return jsonify(error.message), 400

    return {"access_token": access_token}, 200


def signin_professional():

    data = request.get_json()

    try:
        if len(data) > 2 or not 'email' in data.keys() or not 'password' in data.keys():
            raise InvalidKeyError(data)

        professional = ProfessionalModel.query.filter_by(email=data['email']).first()

        if not professional:
            raise EmailNotFoundError(data['email'])

        if not professional.check_password(data['password']):
            raise IncorrectPasswordError()

        access_token = create_access_token(professional)

    except EmailNotFoundError as error:
        return jsonify(error.message), 404
    except IncorrectPasswordError as error:
        return jsonify(error.message), 401
    except InvalidKeyError as error:
        return jsonify(error.message), 400

    return {"access_token": access_token}, 200
