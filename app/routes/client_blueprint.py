from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.client_controllers import create, get_client, get_all,update,delete,schedule_appointment

bp_clients = Blueprint('bp_clients', __name__, url_prefix='/clients')


bp_clients.post('')(create)
bp_clients.get("")(get_all)
bp_clients.patch('')(jwt_required()(update))
bp_clients.delete('')(jwt_required()(delete))
bp_clients.get('/<int:id>')(jwt_required()(get_client))
# bp_clients.post('/user')(jwt_required()(get_by_email))
bp_clients.post('/<int:id>/schedule')(jwt_required()(schedule_appointment))
