from pydantic_core import PydanticCustomError

def validate_str_not_blank(field: str)->str:
    if not field.strip():
        raise PydanticCustomError("blank", "Must not be blank", {"min_length": 1})
    return field