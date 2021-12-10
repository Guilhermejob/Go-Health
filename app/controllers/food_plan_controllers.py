from flask import request, jsonify, current_app
from os import mkdir, path, system
from app.models.client_model import ClientModel
from app.models.food_plan_model import FoodPlanModel

from app.models.professional_model import ProfessionalModel


def create_plan():
    
    pdf = request.files['file']
    professional = ProfessionalModel.query.get(1)
    client = ClientModel.query.get(1)
    
    pdf_path = f"app/archive/{professional.name.lower()}{professional.id}/{client.name.lower()}{client.client_id}/{pdf.filename.lower().replace(' ', '_')}"
    
    send_pdf = FoodPlanModel(pdf=pdf_path, client_id=client.client_id, professional_id=professional.id)
    
    current_app.db.session.add(send_pdf)
    current_app.db.session.commit()
    
    if not path.isdir(f"app/archive/{professional.name.lower()}{professional.id}"):
        mkdir(f"app/archive/{professional.name.lower()}{professional.id}")
    if not path.isdir(f"app/archive/{professional.name.lower()}{professional.id}/{client.name.lower()}{client.client_id}"):
        mkdir(f"app/archive/{professional.name.lower()}{professional.id}/{client.name.lower()}{client.client_id}")
    pdf.save(pdf_path)
    
    
    return jsonify(send_pdf), 201