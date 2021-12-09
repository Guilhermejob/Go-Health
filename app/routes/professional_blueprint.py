from flask import Blueprint
from app.controllers.professional_controllers import create, get_all, get_by_id


bp_professional = Blueprint(
    'bp_professional', __name__, url_prefix='/professional')

bp_professional.post('')(create)
bp_professional.get('')(get_all)
bp_professional.get('/<int:id>')(get_by_id)

bp_teste = Blueprint('bp_teste',__name__)
@bp_teste.get("/")
def testando():
    return {"rotas":{
        "get_all_clients": "/clients",
        "get_client_by_id": "/clients/<int:id>",
        "create_client": "/clients",
        "get_all_professionals": "/professional",
        "get_professional_by_id": "/professional/<int:id>",
        "create_professional": "/professional"
    }},200