from flask import request, jsonify, current_app, send_file
from flask_jwt_extended.utils import get_jwt_identity
from app.controllers import check_user, check_pdf_extension
from app.models.client_model import ClientModel
from app.models.food_plan_model import FoodPlanModel
from app.models.professional_model import ProfessionalModel
from app.exceptions.food_plan_exceptions import InvalidFileError, MissingKeyError, NotFoundError, InvalidKeyValueError
from app.exceptions.client_exceptions import UnauthorizedError
import io


def get_food_plan_by_client_id(client_id: int):
    try:
        check_user(client_id, ClientModel, 'client')
        food_plan = FoodPlanModel.query.filter_by(client_id=client_id).all()

    except NotFoundError as error:
        return jsonify(error.message), 404

    return jsonify(food_plan)


def download_food_plan(food_plan_id: int):
    try:
        food_plan = check_user(food_plan_id, FoodPlanModel, 'archive')

    except NotFoundError as error:
        return jsonify(error.message), 404

    return send_file(io.BytesIO(food_plan.pdf), attachment_filename=food_plan.pdf_name, as_attachment=True)


def create_plan(client_id: int):
    try:

        pdf = request.files
        if not "file" in pdf.keys():
            raise MissingKeyError

        pdf = request.files['file']
        filename = check_pdf_extension(pdf.filename)
        user = get_jwt_identity()

        professional: ProfessionalModel = check_user(
            user['id'], ProfessionalModel, "professional")
        client: ClientModel = check_user(client_id, ClientModel, "client")

        client.check_professional(professional.id)

    except InvalidKeyValueError as error:
        return jsonify(error.message), 400
    except NotFoundError as error:
        return jsonify(error.message), 404
    except InvalidFileError as error:
        return jsonify(error.message), 400
    except UnauthorizedError as error:
        return jsonify(error.message), 401
    except MissingKeyError as error:
        return jsonify(error.message), 400

    send_pdf = FoodPlanModel(pdf_name=filename, pdf=pdf.read(
    ), client_id=client.id, professional_id=professional.id)

    current_app.db.session.add(send_pdf)
    current_app.db.session.commit()

    return jsonify(send_pdf), 201
