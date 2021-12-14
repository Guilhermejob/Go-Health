from flask import jsonify, request, current_app
from app.models.client_model import ClientModel
from app.models.deficiency_model import DeficiencyModel
from app.models.surgery_model import SurgeryModel
from app.models.diseases_model import DiseaseModel
from app.models.calendar_table import CalendarModel
from app.models.professional_model import ProfessionalModel
from app.excepts.professional_exceptions import InvalidDateFormat
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


def create():

    data = request.get_json()

    if data.get('diseases'):
        diseases = data.pop('diseases')

    if data.get('deficiencies'):
        deficiencies = data.pop('deficiencies')

    if data.get('surgeries'):
        surgeries = data.pop('surgeries')

    password_to_hash = data.pop("password")

    data['imc'] = data['weigth']/(data['height'] * data['height'])

    client = ClientModel(**data)
    client.password = password_to_hash

    if diseases:
        disease_list = add_diseases_deficiencies_surgeries(
            diseases, DiseaseModel)
        client.diseases.extend(disease_list)

    if deficiencies:
        deficiency_list = add_diseases_deficiencies_surgeries(
            deficiencies, DeficiencyModel)
        client.deficiencies.extend(deficiency_list)

    if surgeries:
        surgery_list = add_diseases_deficiencies_surgeries(
            surgeries, SurgeryModel)
        client.surgeries.extend(surgery_list)

    current_app.db.session.add(client)
    current_app.db.session.commit()

    return jsonify(client), 201


def get_by_id(id):
    client: ClientModel = ClientModel.query.get(id)
    if not client:
        return {"msg": "Cliente não encontrado"}, 404

    return jsonify(client.serialize()), 200


def get_all():
    all_clients = ClientModel.query.all()
    return jsonify(all_clients), 200


def schedule_appointment(id):

    data = request.get_json()

    try:
        if type(data['schedule_date']) != str:
            raise InvalidDateFormat
    except InvalidDateFormat as error:
        return jsonify(error.message), 409

    schedule_date = data.pop('schedule_date')

    try:
        schedule_date = datetime.strptime(schedule_date, "%d/%m/%Y %H:%M:%S")
    except:
        return jsonify({'msg': 'currect date format : dd/mm/YYYY'}), 409

    schedules_found = CalendarModel.query.filter_by(professional_id=id).all()

    check_false = []

    try:
        professional = ProfessionalModel.query.get_or_404(id)

    except:
        return jsonify({'msg': 'error not found'}), 404

    if schedule_date.isoweekday() == 6 or schedule_date.isoweekday() == 7:
        return jsonify({"msg": 'appointments cannot be scheduled over the weekend'}), 409

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

        current_app.db.session.add(schedule)
        current_app.db.session.commit()

        return jsonify({'msg': 'Horario marcado, nos vemos na consulta!'}), 201
