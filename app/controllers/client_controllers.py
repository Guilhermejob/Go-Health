from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.client_model import ClientModel
from app.models.deficiency_model import DeficiencyModel
from app.models.surgery_model import SurgeryModel
from app.models.diseases_model import DiseaseModel


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


@jwt_required()
def get_by_id(id):
    client: ClientModel = ClientModel.query.get(id)
    if not client:
        return {"msg": "Cliente não encontrado"}, 404

    return jsonify(client.serialize()), 200


@jwt_required()
def get_all():
    all_clients = ClientModel.query.all()
    return jsonify(all_clients), 200
