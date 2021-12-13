class InvalidKeysError(Exception):
    def __init__(self,passed:list,mandatory:list,optional:list):
        self.message = {
            "mandatory keys":mandatory,
            "optional keys": optional,
            "keys sent": passed
        }
        super().__init__(self.message)


class InvalidKeyTypeError(Exception):
    keys = {
        "name":"string",
        "last_name":"string",
        "age":"integer",
        "email":"string",
        "password":"string",
        "gender":"string",
        "height":"float",
        "weigth":"float",
        "optional":{
            "diseases": "[{'name':'string'}]",
            "deficiencies": "[{'name':'string'}]",
            "surgeries": "[{'name':'string'}]"
        }

    }

    received = {
        str: "string",
        int: "integer",
        float: "float",
        list: "list",
        dict: "dictionary",
        bool: "boolean",
    }

    def __init__(self,key,value):
        self.message = {
            "expected": self.keys,
            "received": {
                key: self.received[type(value)]
            }
        }
        super().__init__(self.message)