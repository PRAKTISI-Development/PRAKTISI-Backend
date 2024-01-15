from typing import Any, Dict

def response(status_code: int, success: bool, msg: str, data: Any = None) -> Dict[str, Any]:
    """
    Generate a standardized response dictionary.

    Parameters:
        - status_code (int): HTTP status code.
        - success (bool): Indicates the success of the operation.
        - msg (str): A message describing the result or any error.
        - data (Any): Data payload.

    Returns:
        dict: Standardized response dictionary.
    """
    return {
        'status_code': status_code,
        'success': success,
        'msg': msg,
        'data': data
    }
