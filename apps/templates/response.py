import json

def response(status_code: int, success: bool, msg: str, data):
    payload = [{
        'status_code' : status_code,
        'success'     : success,
        'msg'         : msg,
        'data'        : [data]
    }]

    return json.dumps(payload, indent=2)

data = {
    'nama' : 'Wahyu Kesuma',
    'nim'  : 2109116068,
    'ipk'  : 3.92
}

print(response(200, True, "OK", data))