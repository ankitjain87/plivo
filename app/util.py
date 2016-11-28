from flask import abort, request
from functools import wraps
from sqlalchemy.sql import and_

import models


def login_required():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            auth = request.authorization
            username = auth['username']
            auth_id = auth['password']

            account = models.Account.query.filter(
                and_(models.Account.username == username,
                     models.Account.auth_id == auth_id)).first()

            if not account:
                abort(403)

            return f(account, *args, **kwargs)
        return wrapped
    return wrapper


def length_validation(param, val, min_val=6, max_val=16):
    if param == 'text':
        min_val, max_val = 1, 120

    if len(val) < min_val or len(val) > max_val:
        return {'message': '', 'error': '%s is invalid' % param}
    else:
        return True


def get_param_dict(data_dict):
    param_dict = {}
    for param in ['from', 'to', 'text']:
        param_val = data_dict.get(param, None)
        if not param_val:
            return {'message': '', 'error': '%s is missing' % param}
        else:
            validation = length_validation(param, param_val)
            if type(validation) is not bool:
                return validation
        param_dict[param] = param_val
    return param_dict
