class EmailNotFoundError(Exception):

    def __init__(self, email) -> None:

        self.message = {
            "email": f'{email}',
            "message": "Not registered"
        }

        super().__init__(self.message)


class IncorrectPasswordError(Exception):

    def __init__(self) -> None:

        self.message = {
            "message": "Invalid password"
        }

        super().__init__(self.message)
