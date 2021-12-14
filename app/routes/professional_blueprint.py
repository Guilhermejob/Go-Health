from flask import Blueprint
from app.controllers.professional_controllers import create, delete, get_all, get_by_id, update
from flask_jwt_extended import jwt_required


bp_professional = Blueprint(
    'bp_professional', __name__, url_prefix='/professional')

bp_professional.post('')(jwt_required()(create))
bp_professional.get('')(get_all)
bp_professional.get('/<int:id>')(jwt_required()(get_by_id))
bp_professional.patch('')(jwt_required()(update))
bp_professional.delete('')(jwt_required()(delete))
