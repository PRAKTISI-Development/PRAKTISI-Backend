def check_user_role(user: dict) -> dict:
    userid = user.get('userid', '')
    praktikan = user.get('praktikan')
    asisten_laboratorium = user.get('asisten_laboratorium')
    dosen = user.get('dosen')

    status = (
        'asisten_laboratorium dan praktikan' if len(userid) == 10 and praktikan and asisten_laboratorium
        else 'praktikan' if len(userid) == 10 and praktikan
        else 'asisten_laboratorium' if asisten_laboratorium
        else 'dosen' if len(userid) > 10 and dosen
        else None
    )

    return {'status': status} if status is not None else {}
