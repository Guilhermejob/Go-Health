from flask import jsonify, request, current_app
from app.models.client_model import ClientModel
from app.models.deficiency_model import DeficiencyModel
from app.models.surgery_model import SurgeryModel
from app.models.diseases_model import DiseaseModel


def add_diseases_deficiencies_surgeries(items, model, clientmodel):

    items_list = []

    for item in items:
        found_item = model.query.filter_by(
            name=item['name']).first()
        if found_item == None:
            item_to_add = {
                'name': f"{item['name']}",
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

    data['imc'] = data['weigth']/(data['height'] * data['height'])

    client = ClientModel(**data)

    current_app.db.session.add(client)
    current_app.db.session.commit()

    if diseases:
        disease_list = add_diseases_deficiencies_surgeries(
            diseases, DiseaseModel, client)
        print(disease_list)

    if deficiencies:
        deficiency_list = add_diseases_deficiencies_surgeries(
            deficiencies, DeficiencyModel, client)

    if surgeries:
        surgery_list = add_diseases_deficiencies_surgeries(
            surgeries, SurgeryModel, client)

    return jsonify(client), 201
