from flask import Blueprint
from app.controllers.client_controllers import get_all

bp_clients = Blueprint('bp_clients', __name__, url_prefix='/clients')


bp_clients.get('')(get_all)
