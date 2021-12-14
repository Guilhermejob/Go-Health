from flask import request, jsonify, current_app, send_file
from app.controllers import check_user, check_pdf_extension
from app.models.client_model import ClientModel
from app.models.food_plan_model import FoodPlanModel
from app.models.professional_model import ProfessionalModel
from app.exceptions.food_plan_exceptions import InvalidFileError, NotFoundError, InvalidKeyValueError
import io


def get_food_plan_by_client_id(client_id: int):
    try:
        food_plan = FoodPlanModel.query.filter_by(client_id=client_id).all()
        check_user(client_id, ClientModel, 'client')

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
            return {"message": "missing key 'file'"}, 400

        pdf = request.files['file']
        filename = check_pdf_extension(pdf.filename)

        professional = check_user(1, ProfessionalModel, "professional")
        client = check_user(client_id, ClientModel, "client")

    except InvalidKeyValueError as error:
        return jsonify(error.message), 400
    except NotFoundError as error:
        return jsonify(error.message), 404
    except InvalidFileError as error:
        return jsonify(error.message), 400

    send_pdf = FoodPlanModel(pdf_name=filename, pdf=pdf.read(
    ), client_id=client.id, professional_id=professional.id)

    current_app.db.session.add(send_pdf)
    current_app.db.session.commit()

    return jsonify(send_pdf), 201
