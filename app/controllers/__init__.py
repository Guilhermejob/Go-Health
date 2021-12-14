from app.exceptions.food_plan_exceptions import InvalidFileError, InvalidKeyValueError, NotFoundError
from app.exceptions.client_exceptions import UnauthorizedError
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity


def check_pdf_extension(filename: str):
    extension = filename.split('.')[-1]

    if extension != "pdf":
        raise InvalidFileError(extension)
    return secure_filename(filename)


def check_user(id, model, send_type: str):
    if type(id) != int:
        raise InvalidKeyValueError()

    user = model.query.get(id)
    if not user:
        raise NotFoundError(send_type)

    return user

def check_authorization(id,user_id_key:str):
    user = get_jwt_identity()
    if user[user_id_key] != id:
        raise UnauthorizedError