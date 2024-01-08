def response(status_code: int, success: bool, msg: str, data):
    payload = [{
        'status_code' : status_code,
        'success'     : success,
        'msg'         : msg,
        'data'        : [data]
    }]

    return payload
