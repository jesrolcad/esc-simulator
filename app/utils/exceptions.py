class BadRequestError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
    

class InternalError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class EntityAlreadyExistsError(BadRequestError):
    def __init__(self, entity_name, entity_id, message=None):
        if message is None:
            message = f"{entity_name} with id {entity_id} already exists"
        super().__init__(message)
        self.entity_name = entity_name
        self.entity_id = entity_id


