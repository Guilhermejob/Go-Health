from flask import request, jsonify, current_app, send_file
from os import mkdir, path
from app.models.client_model import ClientModel
from app.models.food_plan_model import FoodPlanModel
from app.models.professional_model import ProfessionalModel
from werkzeug.utils import secure_filename
from app.excepts.professional_exceptions import InvalidFileError, UserNotFoundError, InvalidKeyValueError


def get_food_plan_by_client_id(client_id: int):  
    try:
        food_plan = FoodPlanModel.query.filter_by(client_id=client_id).all()
        check_user(client_id, ClientModel, 'client')

    except UserNotFoundError as e:
        return {"msg":str(e)},404

    return jsonify(food_plan)


def download_food_plan(food_plan_id: int):
    try:
        food_plan = check_user(food_plan_id, FoodPlanModel, 'archive')

    except UserNotFoundError as e:
        return {"msg":str(e)},404

    return send_file(path.realpath(food_plan.pdf), as_attachment=True)


def create_plan():  
    try:
        pdf = request.files['file']
        filename = check_pdf_extension(pdf.filename)

        professional = check_user(1,ProfessionalModel,"professional")
        client = check_user(1,ClientModel,"client")
        
    except InvalidKeyValueError as e:
        return {"msg":str(e)},400
    except UserNotFoundError as e:
        return {"msg":str(e)},404
    except InvalidFileError as e:
        return {"msg":str(e)},400
    
    file_directory_path = create_file_directoy(professional, client)
    pdf_path = f"{file_directory_path}/{filename.lower()}"
    
    send_pdf = FoodPlanModel(pdf=pdf_path, client_id=client.client_id, professional_id=professional.id)
    
    current_app.db.session.add(send_pdf)
    current_app.db.session.commit()
    
    pdf.save(pdf_path)
    
    return jsonify(send_pdf), 201


def create_file_directoy(professional, client):
    professional_path = f"app/archive/{professional.name.lower()}-{professional.id}"
    client_path = f"{client.name.lower()}-{client.client_id}"

    if not path.isdir(professional_path):
        mkdir(professional_path)
    if not path.isdir(f"{professional_path}/{client_path}"):
        mkdir(f"{professional_path}/{client_path}")

    return f"{professional_path}/{client_path}"


def check_pdf_extension(filename:str):
    extension = filename.split('.')[-1]
    if extension != "pdf":
        raise InvalidFileError("The file extension is not a pdf")
    return secure_filename(filename)


def check_user(id,model,user_type:str):
    if type(id) != int:
        raise InvalidKeyValueError("id must be an integer")

    user = model.query.get(id)
    if not user:
        raise UserNotFoundError(f"{user_type} not found")

    return user