class NotFoundProfessionalError(Exception):
    def __init__(self):
        self.message = {"error": "Professional not found!"}

        super().__init__(self.message)


class KeysNotAllowedError(Exception):

    allowed_keys = [
        'name',
        'last_name',
        'gender',
        'age',
        'specialization',
        'description',
        'final_rating',
        'crm',
        'email',
        'password',
        'phone',
    ]

    def __init__(self, key):

        list_keys = [key for key in self.allowed_keys]

        self.message = {
            'error': f"This key: '{key}' not allowed. Keys allowed {list_keys}"
        }

        super().__init__(self.message)


class TypeValueError(Exception):

    def __init__(self, key, value):

        self.message = {
            'error': f"{key}: {value}"
        }

        super().__init__(self.message)


class InvalidDateFormatError(Exception):
    def __init__(self):

        self.message = {
            'error': 'Invalid format! Format valid dd/mm/aaaa!'
        }

        super().__init__(self.message)


class MissingFieldError(Exception):
    def __init__(self):

        self.message = {
            'error': 'Some keys are missing!'
        }

        super().__init__(self.message)


class TypeKeyEmailError(Exception):
    def __init__(self):

        self.message = {
            'error': "Email invalid! Email allowed 'example@mail.com'"
        }

        super().__init__(self.message)


class TypeKeyPhoneError(Exception):
    def __init__(self):

        self.message = {
            'error': "Phone invalid! Phone allowed '(00)00000-0000'"
        }

        super().__init__(self.message)
