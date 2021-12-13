from flask import Blueprint
from app.controllers.login_controllers import signin_client, signin_professional

bp_login = Blueprint('bp_login', __name__, url_prefix='/login')

bp_login.post('/client')(signin_client)
bp_login.post('/professional')(signin_professional)