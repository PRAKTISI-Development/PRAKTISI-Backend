def response(status_code: int, success: bool, msg: str, data):
    return {
        'status_code' : status_code,
        'success'     : success,
        'msg'         : msg,
        'data'        : data
    }
