from flask import Blueprint
from app.controllers.client_controllers import create, get_by_id, get_all,update

bp_clients = Blueprint('bp_clients', __name__, url_prefix='/clients')


bp_clients.post('')(create)
bp_clients.patch('/<int:id>')(update)
bp_clients.get('/<int:id>')(get_by_id)
bp_clients.get("")(get_all)
