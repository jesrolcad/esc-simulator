class BusinessLogicValidationError(Exception):
    def __init__(self, field: str = None, message: str = None):
        if not message:
            message = "Business logic validation error"
        self.field = field
        self.message = message

    def __str__(self):
        return self.message
    
class ValidationError(Exception):
    def __init__(self, field: str = None, message: str = None):
        if not message:
            message = "Validation error"
        self.field = field
        self.message = message

    def __str__(self):
        return self.message
    

class NotFoundError(Exception):
    def __init__(self, field=None, message: str = None):
        if message is None:
            message = "Resource not found"
        self.field = field
        self.message = message

    def __str__(self):
        return self.message


class InternalError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

class AlreadyExistsError(BusinessLogicValidationError):
    def __init__(self, field: str = None, message: str = None, entity_name: str = None, entity_id: int = None):
        if message is None:
            message = f"{entity_name} with id {entity_id} already exists"
        super().__init__(field=field,message=message)
        self.entity_name = entity_name
        self.entity_id = entity_id


