from flask import jsonify, request, current_app
from app.models.professional_model import ProfessionalModel
from app.models.calendar_table import CalendarModel


def create():
    data = request.get_json()

    session = current_app.db.session

    # send hash to db
    password_to_hash = data.pop("password")
    professional = ProfessionalModel(**data)
    professional.password = password_to_hash

    session.add(professional)
    session.commit()

    return jsonify(professional), 200


def get_all():

    professional_list = ProfessionalModel.query.all()

    return jsonify(professional_list), 200


def get_by_id(id):
    professional = ProfessionalModel.query.filter_by(id=id).first()
    return jsonify(professional.serialize()), 200


def get_schedules(id):
    schedules = CalendarModel.query.all()

    schedules_found = [
        schedule for schedule in schedules if schedule.professional_id == id]

    print(schedules_found)

    return jsonify([{'horario': schedule_found.schedule} for schedule_found in schedules_found]), 200
