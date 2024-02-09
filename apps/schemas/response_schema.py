from pydantic import BaseModel
from typing import Optional, Any

class Response(BaseModel):
    status_code: int
    success: bool
    msg: str
    data: Optional[Any] = None