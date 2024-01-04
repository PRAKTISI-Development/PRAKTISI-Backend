import json

def response(msg: str, data: any, success: bool, status_code: int) -> json:
    payload = {
        'success': success,
        'status_code': status_code,
        'message': msg,
        'data': data
    }

    return payload




