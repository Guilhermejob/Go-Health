from flask import jsonify, request, current_app
from app.models.client_model import ClientModel
from app.models.deficiency_model import DeficiencyModel
from app.models.surgery_model import SurgeryModel
from app.models.diseases_model import DiseaseModel
from app.exceptions.client_exceptions import InvalidKeysError
from app.controllers import check_user
from app.exceptions.food_plan_exceptions import NotFoundError


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
    diseases = data.get('diseases',[]) 
    deficiencies = data.get('deficiencies',[])
    surgeries = data.get('surgeries',[])

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

    return diseases,deficiencies,surgeries


def check_data_keys(data):
    if (len(data) < len(ClientModel.mandatory_keys)) or (len(data) > (len(ClientModel.mandatory_keys) + len(ClientModel.optional_keys))):
        raise InvalidKeysError(list(data.keys()),ClientModel.mandatory_keys,ClientModel.optional_keys)

    for key in ClientModel.mandatory_keys:
        if key not in data.keys():
            raise InvalidKeysError(list(data.keys()),ClientModel.mandatory_keys,ClientModel.optional_keys)

    for key in data.keys():
        if((key not in ClientModel.mandatory_keys) and (key not in ClientModel.optional_keys)):
            raise InvalidKeysError(list(data.keys()),ClientModel.mandatory_keys,ClientModel.optional_keys)
    
    # return data

# def check_data_values(data):
#     return True


def create():

    data = request.get_json()
    
    try:
        check_data_keys(data)

        diseases,deficiencies,surgeries = get_diseases_deficiencies_surgeries(data)

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

    return jsonify(client), 201


def get_by_id(id):
    try:
        client = check_user(id,ClientModel,"client")
    except NotFoundError as error:
        return jsonify(error.message),404

    return jsonify(client.serialize()), 200


def get_all():
    all_clients = ClientModel.query.all()
    return jsonify(all_clients), 200
