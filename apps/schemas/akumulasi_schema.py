from pydantic import BaseModel, Field
from typing import Optional, Dict

#on progress
class StudentSchema(BaseModel):
    NIM: Optional[str]
    nama_lengkap: Optional[str]
    semester: Optional[str]
    praktikum: Optional[str]
    kehadiran: Optional[float]
    proyek_akhir: Optional[float]
    nilai_akhir: Optional[float]

def generate_dynamic_schema(data: Dict[str, Optional[float]]) -> BaseModel:
    """Generate a dynamic Pydantic schema based on the provided data."""
    dynamic_fields = {}
    for key, value in data.items():
        dynamic_fields[key] = (Optional[type(value)], Field(value, alias=key))

    # Generate a class name dynamically
    class_name = "DynamicStudentSchema"
    dynamic_schema = type(class_name, (BaseModel,), dynamic_fields)

    return dynamic_schema