from pydantic import BaseModel, Field
from typing import Optional, Dict

def generate_dynamic_schema(data: Dict[str, Optional[float]]) -> BaseModel:
    """Generate a dynamic Pydantic schema based on the provided data."""
    dynamic_fields = {}
    for key, value in data.items():
        dynamic_fields[key] = (Optional[type(value)], Field(value, alias=key))

    class_name = "DynamicStudentSchema"
    dynamic_schema = type(class_name, (BaseModel,), dynamic_fields)

    return dynamic_schema