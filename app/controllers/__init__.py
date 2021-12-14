from app.exceptions.food_plan_exceptions import InvalidFileError, InvalidKeyValueError, NotFoundError
from werkzeug.utils import secure_filename


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


def format_output_especific_professional(text):
    output = text.replace('(', ' ')
    output = output.replace(')', ' ')
    output = output.lstrip()

    return output
