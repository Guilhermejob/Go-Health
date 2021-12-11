from flask import jsonify, current_app, request
from app.models.professional_rating_model import ProfessionalRatingModel
from app.models.client_model import ClientModel
from app.models.professional_model import ProfessionalModel

def set_rating(id):
    data = request.get_json()
    # fazer função de jwt
    client = ClientModel.query.get(1)
    professional = ProfessionalModel.query.get(id)

    rating = ProfessionalRatingModel(rating = data["rating"], client_id = client.client_id, professional_id = professional.id)

    current_app.db.session.add(rating)

    rating_output = professional.rating

    average = sum([rating.rating for rating in rating_output]) / len(rating_output)

    professional.final_rating = average

    current_app.db.session.add(professional)
    current_app.db.session.commit()
    
    return jsonify(rating)