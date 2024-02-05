from typing import Any, Dict,List
from fastapi.responses import JSONResponse
from sqlalchemy.orm import attributes
from fastapi import Request
from pydantic import BaseModel
from typing import Optional

class ResponseModel(BaseModel):
    status_code: int
    success: bool
    msg: str
    data: Optional[Any] = None

def response(request: Request, status_code: int, success: bool, msg: str, data: Any = None) -> Dict[str, Any]:
    """
    Generate a standardized response dictionary.

    Parameters:
        - request (Request): The FastAPI Request object.
        - status_code (int): HTTP status code.
        - success (bool): Indicates the success of the operation.
        - msg (str): A message describing the result or any error.
        - data (Any): Data payload.

    Returns:
        JSON or Dict: Standardized response JSON or dictionary.
    """
    response_dict = ResponseModel(
        status_code= status_code,
        success= success,
        msg= msg,
        data= data
    )
    
    if data is None:
        return JSONResponse(content=response_dict.__dict__)
    
    elif request.method == "POST" and data is not None:
        instance_dict = attributes.instance_dict(data)
        instance_dict.pop('_sa_instance_state', None)
        response_dict.data = instance_dict
        return JSONResponse(content=response_dict.__dict__)
    else:
        return response_dict.__dict__