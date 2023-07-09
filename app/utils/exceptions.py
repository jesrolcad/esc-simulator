class BusinessLogicValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message

    def __str__(self):
        return self.message
    

class NotFoundError(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = "Resource not found"
        self.message = message

    def __str__(self):
        return self.message


class InternalError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

class AlreadyExistsError(BusinessLogicValidationError):
    def __init__(self, entity_name: str = None, entity_id: int = None, message:str = None):
        if message is None:
            message = f"{entity_name} with id {entity_id} already exists"
        super().__init__(message)
        self.entity_name = entity_name
        self.entity_id = entity_id


