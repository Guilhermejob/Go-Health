from flask import jsonify, request, current_app
from app.models.client_model import ClientModel
from app.models.deficiency_model import DeficiencyModel
from app.models.surgery_model import SurgeryModel
from app.models.diseases_model import DiseaseModel


def add_diseases_deficiencies_surgeries(items, model, client_id):

    items_list = []

    for item in items:
        item_to_add = {
            'name': f"{item['name']}",
            'client_id': client_id
        }
        found_item = model(**item_to_add)
        current_app.db.session.add(found_item)
        current_app.db.session.commit()

        items_list.append(found_item)

    return items_list


def create_client():

    data = request.get_json()

    diseases = data.pop('disease')
    deficiencies = data.pop('deficiency')
    surgeries = data.pop('surgery')
    password_to_hash = data.pop("password")

    data['imc'] = data['weigth']/(data['height'] * data['height'])

    client = ClientModel(**data)
    client.password = password_to_hash

    current_app.db.session.add(client)
    current_app.db.session.commit()

    if diseases:
        disease_list = add_diseases_deficiencies_surgeries(
            diseases, DiseaseModel, client.client_id)
    if deficiencies:
        deficiency_list = add_diseases_deficiencies_surgeries(
            deficiencies, DeficiencyModel, client.client_id)
    if surgeries:
        surgery_list = add_diseases_deficiencies_surgeries(
            surgeries, SurgeryModel, client.client_id)

    return jsonify(client), 201


def get_client(id):
    client: ClientModel = ClientModel.query.get(id)

    if not client:
        return {"msg": "Cliente não encontrado"}, 404

    return jsonify({
        "name": client.name,
        "last_name": client.last_name,
        "age": client.age,
        "email": client.email,
        "gender": client.gender,
        "height": client.height,
        "weigth": client.weigth,
        "imc": client.imc,
        "diseases": [{"name": disease.name} for disease in client.diseases],
        "surgeries": [{"name": surgery.name} for surgery in client.surgeries],
        "deficiencies": [{"name": deficiency.name} for deficiency in client.deficiencies]
    }), 200
