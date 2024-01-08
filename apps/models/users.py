from typing import Optional
from pydantic import BaseModel

class TokenData(BaseModel):
    nim: Optional[str] = None
    tipe_user: Optional[str] = None
