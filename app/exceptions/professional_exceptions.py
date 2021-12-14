class NotFoundProfessionalError(Exception):
    def __init__(self):
        self.message = {"error": "Professional not found!"}

        super().__init__(self.message)
