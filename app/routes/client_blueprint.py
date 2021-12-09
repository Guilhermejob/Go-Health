from flask import Blueprint
from app.controllers.client_controllers import create_client,get_client

bp_clients = Blueprint('bp_clients', __name__, url_prefix='/clients')


bp_clients.post('')(create_client)
bp_clients.get('/<int:id>')(get_client)
