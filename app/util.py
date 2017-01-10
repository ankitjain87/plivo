from flask import abort, request
from functools import wraps
from sqlalchemy.sql import and_

import models


def login_required():
    """Decorator to do the authentication for the requested user."""
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


def length_validation(val, min_val=6, max_val=16):
    """Length validation for the parameter."""
    if len(val) < min_val or len(val) > max_val:
        return False
    else:
        return True


def get_param_dict(data_dict):
    """Returns a parameter dict after validation."""
    param_dict = {}
    for param in ['from', 'to', 'text']:
        param_val = data_dict.get(param, None)
        if not param_val:
            return {'message': '', 'error': '%s is missing' % param}
        else:
            validation = False
            if param == 'text':
                validation = length_validation(param_val, min_val=1, max_val=120)
            else:
                validation = length_validation(param_val)
            if not validation:
                return {'message': '', 'error': '%s is invalid' % param}
        param_dict[param] = param_val
    return param_dict
