from flask import Blueprint
from app.controllers.professional_rating_controllers import set_rating
from flask_jwt_extended import jwt_required


bp_professional_rating = Blueprint(
    'bp_professional_rating', __name__, url_prefix='/professional_rating')

bp_professional_rating.post('<int:professional_id>')(jwt_required()(set_rating))