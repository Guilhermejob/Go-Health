from flask import jsonify, current_app, request
from app.exceptions.professional_exceptions import NotFoundProfessionalError
from app.exceptions.rating_exceptions import AlreadyRatingError, InvalidKeyError, InvalidTypeError
from app.models.professional_rating_model import ProfessionalRatingModel
from app.models.professional_model import ProfessionalModel
from flask_jwt_extended import get_jwt_identity

def set_rating(professional_id: int):
    data = request.get_json()
    
    try:
        if len(data) > 1 or not 'rating' in data.keys():
            raise InvalidKeyError(data)

        if type(data['rating']) != int:
            raise InvalidTypeError(data['rating'])

        client = get_jwt_identity()
        professional = ProfessionalModel.query.get(professional_id)
        
        if not professional:
            raise NotFoundProfessionalError
        
        verify_rating = ProfessionalRatingModel.query.filter_by(client_id=client['client_id']).first()
        
        print(verify_rating)
        
        if verify_rating:
            raise AlreadyRatingError
        
        rating = ProfessionalRatingModel(rating = data['rating'], client_id = client['client_id'], professional_id = professional.id)

        current_app.db.session.add(rating)

        rating_output = professional.rating

        average = sum([rating.rating for rating in rating_output]) / len(rating_output)

        professional.final_rating = average

        current_app.db.session.add(professional)
        current_app.db.session.commit()

    except NotFoundProfessionalError as error:
        return jsonify(error.message), 404
    except InvalidTypeError as error:
        return jsonify(error.message), 400
    except InvalidKeyError as error:
        return jsonify(error.message), 400
    except AlreadyRatingError as error:
        return jsonify(error.message), 409
    
    return jsonify(rating), 200