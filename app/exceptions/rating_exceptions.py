class InvalidTypeError(Exception):

    types = {
        str: "string",
        int: "integer",
        float: "float",
        list: "list",
        dict: "dictionary",
        bool: "boolean"
    }
    
    
    def __init__(self, rating) -> None:
        if type(rating) != int:
            self.message = {
                "available field": {
                    "rating": "integer"
                },
                "field sent": {
                    "rating": f'{self.types[type(rating)]}'
                }
            }
        super().__init__(self.message)
        
        
class InvalidKeyError(Exception):
    
    
    def __init__(self, data) -> None:
        self.message = {
            "available key": {
                "rating": "integer"
            },
            "key sent": [
                {
                    "key": key
                } for key in data
            ]
        }
        super().__init__(self.message)
        
        
class AlreadyRatingError(Exception):
    
    
    def __init__(self) -> None:
        self.message = {
            "message": "Professional has already received rating from this client."
        }
        super().__init__(self.message)