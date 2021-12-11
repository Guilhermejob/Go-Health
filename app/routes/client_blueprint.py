from flask import Blueprint
from app.controllers.client_controllers import create, get_by_id, get_all, schedule_appointment

bp_clients = Blueprint('bp_clients', __name__, url_prefix='/clients')


bp_clients.post('')(create)

bp_clients.get('/<int:id>')(get_by_id)
bp_clients.get("")(get_all)
bp_clients.post('/<int:id>/schedule')(schedule_appointment)
