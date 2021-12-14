from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.client_model import ClientModel
from app.models.deficiency_model import DeficiencyModel
from app.models.surgery_model import SurgeryModel
from app.models.diseases_model import DiseaseModel
from app.exceptions.client_exceptions import InvalidKeysError, InvalidValueTypeError, InvalidGenderValueError, InvalidEmailError
from app.controllers import check_user
from app.exceptions.food_plan_exceptions import NotFoundError
from sqlalchemy.exc import IntegrityError


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


def check_update_keys(data):
    for key in data.keys():
        if((key not in ClientModel.mandatory_keys) and (key not in ClientModel.optional_keys)):
            raise InvalidKeysError(list(data.keys()),ClientModel.mandatory_keys,ClientModel.optional_keys)


def check_data_keys(data):
    if (len(data) < len(ClientModel.mandatory_keys)) or (len(data) > (len(ClientModel.mandatory_keys) + len(ClientModel.optional_keys))):
        raise InvalidKeysError(list(data.keys()),ClientModel.mandatory_keys,ClientModel.optional_keys)

    for key in ClientModel.mandatory_keys:
        if key not in data.keys():
            raise InvalidKeysError(list(data.keys()),ClientModel.mandatory_keys,ClientModel.optional_keys)

    check_update_keys(data)
  

def check_data_values(data):

    # "name","last_name","age","email","password","gender","height","weigth"
    for key,value in data.items():
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
        
        # "diseases","surgeries","deficiencies" - [{"name":"string"}]
        if (key == "diseases" or key == "surgeries" or key == "deficiencies"):
            if type(value) != list:
                raise InvalidValueTypeError(data)
            
            if(len(value)>0):
                for item in value:
                    if(
                        (type(item) != dict) or 
                        (len(item) != 1) or 
                        ("name" not in item.keys()) or 
                        type(item["name"]) != str
                    ):
                        raise InvalidValueTypeError(data)


def check_gender(gender:str):
    if ((gender.lower() != 'm') and (gender.lower() != 'f')):
        raise InvalidGenderValueError


def check_email(email:str):
    if not (("@" in email) and ("." in email.split("@")[-1])):
        raise InvalidEmailError


def update(id):
    data = request.get_json()
    try:
        check_update_keys(data)
        check_data_values(data)
        if data.get("gender"):
            check_gender(data["gender"])
        if data.get("email"):
            check_email(data["email"])

        diseases,deficiencies,surgeries = get_diseases_deficiencies_surgeries(data)
        if diseases:
            data["diseases"] = diseases
        if deficiencies:
            data["deficiencies"] = deficiencies
        if surgeries:
            data["surgeries"] = surgeries

        client = check_user(id,ClientModel,"client")

        new_password = data.get("password") 
        if new_password:
            client.password = new_password
            data.pop("password")

        for key,value in data.items():
            setattr(client,key,value)

        current_app.db.session.add(client)
        current_app.db.session.commit()

    except NotFoundError as error:
        return jsonify(error.message),404
    except InvalidKeysError as error:
        return jsonify(error.message), 400
    except InvalidValueTypeError as error:
        return jsonify(error.message), 400
    except InvalidEmailError as error:
        return jsonify(error.message), 400
    except InvalidGenderValueError as error:
        return jsonify(error.message), 400
    except IntegrityError:
        return jsonify({"message":"email already exists"}),409

    return jsonify(client),201


def create():
    data = request.get_json()
    
    try:
        check_data_keys(data)
        check_data_values(data)
        check_gender(data["gender"])
        check_email(data["email"])

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
    except InvalidValueTypeError as error:
        return jsonify(error.message), 400
    except InvalidEmailError as error:
        return jsonify(error.message), 400
    except InvalidGenderValueError as error:
        return jsonify(error.message), 400
    except IntegrityError:
        return jsonify({"message":"email already exists"}),409
    
    return jsonify(client), 201


@jwt_required()
def get_by_id(id):
    try:
        client = check_user(id,ClientModel,"client")
    except NotFoundError as error:
        return jsonify(error.message),404

    return jsonify(client.serialize()), 200


@jwt_required()
def get_all():
    all_clients = ClientModel.query.all()
    return jsonify(all_clients), 200
