from sqlalchemy.orm.base import EXT_CONTINUE


class MultipleKeysFreeSchedulesError(Exception):
    def __init__(self):
        self.message = {
            "error": "have more keys than necessary",
            "required_keys": "schedule_date"
        }
        super().__init__(self.message)


class MissingKeyError(Exception):
    def __init__(self):
        self.message = {
            "error": "missing a required key",
            "required_keys": "schedule_date"
        }
        super().__init__(self.message)


class ProfessionalNotFoundError(Exception):
    def __init__(self):
        self.message = {
            "error": "Professional not found"
        }
        super().__init__(self.message)


class ProfessionalScheduleListError(Exception):
    def __init__(self):
        self.message = {
            "message": "professional doesn't have an appointment yet"
        }
        super().__init__(self.message)


class WeekendAppointmentsError(Exception):
    def __init__(self):
        self.message = {
            "message": "appointments cannot be scheduled over the weekend"
        }
        super().__init__(self.message)


class OutsideOfficeHoursError(Exception):
    def __init__(self):
        self.message = {
            "message": "We do not make an appointment at this time",
            "schedules:ours": 'scheduling hours from 9:00 am to 5:15 pm'
        }
        super().__init__(self.message)


class TypeDateNotAllowedError(Exception):
    def __init__(self):
        self.message = {
            "error": "The date must be passed in string",
        }
        super().__init__(self.message)


class FormatDateError(Exception):
    def __init__(self):
        self.message = {
            "error": "currect date format : dd/mm/YYYY",
        }
        super().__init__(self.message)
