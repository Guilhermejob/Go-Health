class InvalidFileError(Exception):


    def __init__(self, filename: str) -> None:

        self.message = {
                "available extension": {
                    "message": ".pdf"
                },
                "extension sent": {
                    "message": f".{filename}"
                }
            }

        super().__init__(self.message)


class NotFoundError(Exception):


    def __init__(self, send_type: str) -> None:

        self.message = {
            "message": f"{send_type} not found"
        }

        super().__init__(self.message)


class InvalidKeyValueError(Exception):


    def __init__(self) -> None:

        self.message = {
            "message": "id must be an integer"
        }

        super().__init__(self.message)
    