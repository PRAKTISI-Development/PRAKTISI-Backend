from typing import Any, Dict, List  
from fastapi.responses import JSONResponse
from sqlalchemy.orm import attributes
from fastapi import Request

# def post_response(status_code: int, success: bool, msg: str, data: Any) -> Dict[str, Any]:
#     """
#     Generate a standardized response dictionary.

#     Parameters:
#         - status_code (int): HTTP status code.
#         - success (bool): Indicates the success of the operation.
#         - msg (str): A message describing the result or any error.
#         - data (Any): Data payload.

#     Returns:
#         JSON: Standardized response JSON.
#     """
#     return JSONResponse({
#         'status_code': status_code,
#         'success'    : success,
#         'msg'        : msg,
#         'data'       : data
#     })


# def response(status_code: int, success: bool, msg: str, data: List) -> Dict[str,Any]:
#     """
#     Generate a standardized response dictionary.

#     Parameters:
#         - status_code (int): HTTP status code.
#         - success (bool): Indicates the success of the operation.
#         - msg (str): A message describing the result or any error.
#         - data (Any): Data payload.

#     Returns:
#         JSON: Standardized response JSON.
#     """
#     return {
#         'status_code': status_code,
#         'success'    : success,
#         'msg'        : msg,
#         'data'       : data
#     }

def response(request: Request, status_code: int, success: bool, msg: str, data: Any) -> Dict[str, Any]:
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
    response_dict = {
        'status_code': status_code,
        'success': success,
        'msg': msg,
        'data': data
    }

    if request.method == "POST":
        instance_dict = attributes.instance_dict(data)
        instance_dict.pop('_sa_instance_state', None)
        response_dict['data'] = instance_dict
        return JSONResponse(content=response_dict)
    else:
        return response_dict