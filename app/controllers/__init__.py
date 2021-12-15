from app.exceptions.food_plan_exceptions import InvalidFileError, InvalidKeyValueError, NotFoundError
from app.exceptions.professional_exceptions import KeysNotAllowedError, TypeValueError, MissingFieldError
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


def validate_keys_professional(data):

    allowed_keys = [
        'name',
        'last_name',
        'gender',
        'age',
        'specialization',
        'description',
        'final_rating',
        'crm',
        'email',
        'password',
        'phone',
    ]

    for key in data.keys():
        if key not in allowed_keys:
            raise KeysNotAllowedError(data, key)


def validate_type_value_professional(data):

    for key, value in data.items():
        if type(value) != str and type(value) != int:
            raise TypeValueError(key, value)


def check_all_fields_professional(data):
    allowed_keys = [
        'name',
        'last_name',
        'gender',
        'age',
        'specialization',
        'description',
        'final_rating',
        'crm',
        'email',
        'password',
        'phone',
    ]

    keys = [key for key in data.keys()]

    if len(allowed_keys) > len(keys):
        raise MissingFieldError
