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
    def __init__(self, entity_name, entity_id):
        super().__init__(f"{entity_name} with id {entity_id} already exists")
        self.entity_name = entity_name
        self.entity_id = entity_id


if __name__ == "__main__":
    raise EntityAlreadyExistsError("Country", 1)


