class InvalidFileError(Exception):
    ...


class UserNotFoundError(Exception):
    ...


class InvalidKeyValueError(Exception):
    ...


class InvalidDateFormat(Exception):
    def __init__(self):
        self.message = {
            'err': 'the date has to be passed in string',

        }
        super().__init__(self.message)
