import re
from flask import jsonify, request, current_app
from flask_jwt_extended.utils import get_jwt_identity
from app.models.client_model import ClientModel
from app.models.deficiency_model import DeficiencyModel
from app.models.surgery_model import SurgeryModel
from app.models.diseases_model import DiseaseModel
from app.exceptions.client_exceptions import InvalidKeysError, InvalidValueTypeError, InvalidGenderValueError, InvalidEmailError
from app.exceptions.schedules_exceptions import FormatDateError, OutsideOfficeHoursError, ProfessionalNotFoundError, TypeDateNotAllowedError, WeekendAppointmentsError, MultipleKeysFreeSchedulesError, MissingKeyError
from app.controllers import check_user
from app.exceptions.food_plan_exceptions import NotFoundError
from sqlalchemy.exc import IntegrityError
from re import S, fullmatch
from app.models.calendar_table import CalendarModel
from app.models.professional_model import ProfessionalModel
from app.exceptions.professional_exceptions import InvalidDateFormatError
from datetime import *


def add_diseases_deficiencies_surgeries(items, model):

    items_list = []

    for item in items:
        item_to_add = model.query.filter(
            model.name.ilike(f"%{item['name']}%")).first()

        if not item_to_add:
            item_to_add = {'name': f"{item['name']}"}
            new_item = model(**item_to_add)

            current_app.db.session.add(new_item)
            current_app.db.session.commit()
            item_to_add = model.query.filter(
                model.name.ilike(f"%{item['name']}%")).first()

        items_list.append(item_to_add)

    return items_list


def get_diseases_deficiencies_surgeries(data):
    diseases = data.get('diseases', [])
    deficiencies = data.get('deficiencies', [])
    surgeries = data.get('surgeries', [])

    if diseases:
        data.pop('diseases')
        diseases = add_diseases_deficiencies_surgeries(
            diseases, DiseaseModel)

    if deficiencies:
        data.pop('deficiencies')
        deficiencies = add_diseases_deficiencies_surgeries(
            deficiencies, DeficiencyModel)

    if surgeries:
        data.pop('surgeries')
        surgeries = add_diseases_deficiencies_surgeries(
            surgeries, SurgeryModel)

    return diseases, deficiencies, surgeries


def check_update_keys(data):
    for key in data.keys():
        if((key not in ClientModel.mandatory_keys) and (key not in ClientModel.optional_keys)):
            raise InvalidKeysError(
                list(data.keys()), ClientModel.mandatory_keys, ClientModel.optional_keys)


def check_create_data_keys(data):
    if (len(data) < len(ClientModel.mandatory_keys)) or (len(data) > (len(ClientModel.mandatory_keys) + len(ClientModel.optional_keys))):
        raise InvalidKeysError(
            list(data.keys()), ClientModel.mandatory_keys, ClientModel.optional_keys)

    for key in ClientModel.mandatory_keys:
        if key not in data.keys():
            raise InvalidKeysError(
                list(data.keys()), ClientModel.mandatory_keys, ClientModel.optional_keys)

    check_update_keys(data)


def check_data_values(data):

    for key, value in data.items():
        if ((
            key == "name" or
            key == "last_name" or
            key == "email" or
            key == "password" or
            key == "gender"
        ) and type(value) != str):
            raise InvalidValueTypeError(data)

        if((key == "height" or key == "weigth") and type(value) != float):
            raise InvalidValueTypeError(data)

        if key == "age" and type(value) != int:
            raise InvalidValueTypeError(data)

        if (key == "diseases" or key == "surgeries" or key == "deficiencies"):
            if type(value) != list:
                raise InvalidValueTypeError(data)

            if(len(value) > 0):
                for item in value:
                    if(
                        (type(item) != dict) or
                        (len(item) != 1) or
                        ("name" not in item.keys()) or
                        type(item["name"]) != str
                    ):
                        raise InvalidValueTypeError(data)


def check_gender(gender: str):
    if ((gender.lower() != 'm') and (gender.lower() != 'f')):
        raise InvalidGenderValueError


def check_email(email: str):
    pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    is_valid = fullmatch(pattern, email)
    if not is_valid:
        raise InvalidEmailError


def update():

    data = request.get_json()
    user = get_jwt_identity()

    try:
        check_update_keys(data)
        check_data_values(data)
        if data.get("gender"):
            check_gender(data["gender"])
        if data.get("email"):
            check_email(data["email"])

        diseases, deficiencies, surgeries = get_diseases_deficiencies_surgeries(
            data)
        if diseases:
            data["diseases"] = diseases
        if deficiencies:
            data["deficiencies"] = deficiencies
        if surgeries:
            data["surgeries"] = surgeries

        client = check_user(user["id"], ClientModel, "client")

        new_password = data.get("password")
        if new_password:
            client.password = new_password
            data.pop("password")

        for key, value in data.items():
            setattr(client, key, value)

        current_app.db.session.add(client)
        current_app.db.session.commit()

    except NotFoundError as error:
        return jsonify(error.message), 404
    except InvalidKeysError as error:
        return jsonify(error.message), 400
    except InvalidValueTypeError as error:
        return jsonify(error.message), 400
    except InvalidEmailError as error:
        return jsonify(error.message), 400
    except InvalidGenderValueError as error:
        return jsonify(error.message), 400
    except IntegrityError:
        return jsonify({"message": "email already exists"}), 409

    result = client.serialize()
    result.pop("food_plan")
    result.pop("professional")

    return jsonify(result), 201


def create():
    data = request.get_json()

    try:
        check_create_data_keys(data)
        check_data_values(data)
        check_gender(data["gender"])
        check_email(data["email"])

        diseases, deficiencies, surgeries = get_diseases_deficiencies_surgeries(
            data)

        password_to_hash = data.pop("password")

        data['imc'] = data['weigth']/(data['height'] * data['height'])

        client = ClientModel(**data)
        client.password = password_to_hash

        client.diseases.extend(diseases)
        client.deficiencies.extend(deficiencies)
        client.surgeries.extend(surgeries)

        current_app.db.session.add(client)
        current_app.db.session.commit()

    except InvalidKeysError as error:
        return jsonify(error.message), 400
    except InvalidValueTypeError as error:
        return jsonify(error.message), 400
    except InvalidEmailError as error:
        return jsonify(error.message), 400
    except InvalidGenderValueError as error:
        return jsonify(error.message), 400
    except IntegrityError:
        return jsonify({"message": "email already exists"}), 409

    return jsonify(client), 201


def get_client(id):

    try:
        client = check_user(id, ClientModel, 'client')

    except NotFoundError as err:
        return jsonify(err.message), 404

    return jsonify(client.serialize()), 200


def get_all():
    all_clients = ClientModel.query.all()
    return jsonify(all_clients), 200


def delete():
    try:
        user = get_jwt_identity()
        client = check_user(user["id"], ClientModel, "client")
        current_app.db.session.delete(client)
        current_app.db.session.commit()

    except NotFoundError as error:
        return jsonify(error.message), 404

    return "", 204


def get_schedules(id):
    schedules = CalendarModel.query.all()

    schedules_found = [
        schedule for schedule in schedules if schedule.client_id == id]

    return jsonify([{'horario': schedule_found.schedule} for schedule_found in schedules_found]), 200


def schedule_appointment(id):

    data = request.get_json()

    try:
        if "schedule_date" not in data.keys():
            raise MissingKeyError

        if len(data.keys()) > 1:
            raise MultipleKeysFreeSchedulesError

    except MultipleKeysFreeSchedulesError as error:
        return jsonify(error.message), 400

    except MissingKeyError as error:
        return jsonify(error.message), 400

    user = get_jwt_identity()

    data['professional_id'] = id

    data['client_id'] = user['id']

    try:

        if type(data['schedule_date']) != str:
            print("aaaaaaaaaaaaaaaaaa")
            raise TypeDateNotAllowedError

        schedule_date = data.pop('schedule_date')

        try:
            schedule_date = datetime.strptime(
                schedule_date, "%d/%m/%Y %H:%M:%S")

        except:
            return jsonify({"error": "currect date format : dd/mm/YYYY"}), 409

        if schedule_date.hour < 9 or schedule_date.hour > 17:
            raise OutsideOfficeHoursError

    except TypeDateNotAllowedError as error:
        return jsonify(error.message), 409

    except OutsideOfficeHoursError as error:
        return jsonify(error.message), 200

    schedules_found = CalendarModel.query.filter_by(professional_id=id).all()

    check_false = []

    try:
        professional = ProfessionalModel.query.get(id)

        if professional == None:
            raise ProfessionalNotFoundError

        if schedule_date.isoweekday() == 6 or schedule_date.isoweekday() == 7:
            raise WeekendAppointmentsError

    except WeekendAppointmentsError as error:
        return jsonify(error.message), 200

    except ProfessionalNotFoundError as error:
        return jsonify(error.message), 404

    else:
        for schedule_found in schedules_found:

            check_schedule = (datetime.strptime(
                str(schedule_found.schedule), "%Y-%m-%d %H:%M:%S"))

            value = schedule_date != check_schedule

            check_false.append(value)

    if False in check_false:

        return jsonify({'msg': 'busy schedule'}), 409
    else:
        data['schedule'] = schedule_date

        schedule = CalendarModel(**data)

        # client.professional_id = professional.id
        # current_app.db.session.add(client)

        current_app.db.session.add(schedule)
        current_app.db.session.commit()

        return jsonify({'msg': 'Horario marcado, nos vemos na consulta!'}), 201
