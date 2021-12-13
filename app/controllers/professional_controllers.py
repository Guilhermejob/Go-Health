from flask import jsonify, request, current_app
from app.models.professional_model import ProfessionalModel
from app.models.calendar_table import CalendarModel
from datetime import *


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


def get_free_schedules(id):

    free_hours = []

    busy_schedule = []

    free_schedules = []

    data = request.get_json()

    try:
        professional = ProfessionalModel.query.get_or_404(id)

    except:
        return jsonify({'msg': 'error not found'}), 404

    try:
        schedule_date = datetime.strptime(data['schedule_date'], "%d/%m/%Y")
    except:
        return jsonify({'msg': 'currect date format : dd/mm/YYYY'})

    schedule_date = schedule_date + timedelta(hours=9)

    schedules = CalendarModel.query.filter_by(professional_id=id).all()

    if len(schedules) > 0:

        for schedule_found in schedules:
            date = (datetime.strptime(
                str(schedule_found.schedule), "%Y-%m-%d %H:%M:%S"))
            busy_schedule.append(date)

    while schedule_date.hour < 17.15:
        free_hours.append(schedule_date)
        schedule_date += timedelta(minutes=45)

    for hour in free_hours:

        if hour not in busy_schedule:
            free_schedules.append(hour)

    return jsonify([{'horario': schedule_found} for schedule_found in free_schedules]), 200
