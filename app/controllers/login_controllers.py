from flask import request
from flask_jwt_extended import create_access_token
from app.models.client_model import ClientModel
from app.models.professional_model import ProfessionalModel

def signin_client():
    
    data = request.get_json()
    
    formatted_email = f"%{data['email']}%"
    client = ClientModel.query.filter(ClientModel.email.ilike(formatted_email)).first()
    
    if not client:
        return {"message": "client not found"}, 404
    
    if client.check_password(data['password']):
        access_token = create_access_token(client)
        return {"access_token": access_token}, 200
    else:
        return {"message": "Email or password do not match."}, 401
    

def signin_professional():
    
    data = request.get_json()
    
    formatted_email = f"%{data['email']}%"
    professional = ProfessionalModel.query.filter(ProfessionalModel.email.ilike(formatted_email)).first()
    
    if not professional:
        return {"message": "professional not found"}, 404
    
    if professional.check_password(data['password']):
        access_token = create_access_token(professional)
        return {"access_token": access_token}, 200
    else:
        return {"message": "Email or password do not match."}, 401