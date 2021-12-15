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
