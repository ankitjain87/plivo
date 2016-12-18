from flask import abort, jsonify, request
from sqlalchemy.sql import and_
from app import cache

import cPickle
from datetime import datetime
import logging

import config
import models
from util import get_param_dict, login_required


def index():
    return "Hello, World!"


@login_required()
def inbound(account):
    """Inbound sms.

    Args:
        account: User account.

    Returns:
        A dict with message and error based on the given parameters.

    """
    if request.method != 'POST':
        abort(405, "Only Post allowed.")

    try:
        param_dict = get_param_dict(request.json)
        if 'error' in param_dict:
            return jsonify(param_dict)

        phone_number = models.PhoneNumber.query.filter(
            and_(models.PhoneNumber.number == param_dict['to'],
                 models.PhoneNumber.account_id == account.id)).first()

        if not phone_number:
            return jsonify({'message': '', 'error': 'to parameter not found'})

        if param_dict['text'] in ['STOP', 'STOP\n', 'STOP\r', 'STOP\r\n']:
            cache.set(
                {param_dict['from']: param_dict['to']}, 1, config.CACHE_EXPIRE)

        return jsonify({'message': 'inbound sms ok', 'error': ''})
    except Exception as ex:
        logging.info(ex)
        return jsonify({'message': '', 'error': 'unknown failure'})


@login_required()
def outbound(account):
    """Outbound sms.

    Args:
        account: User account.

    Returns:
        A dict with message and error based on the given parameters.

    """
    if request.method != 'POST':
        abort(405, "Only Post allowed.")

    try:
        param_dict = get_param_dict(request.json)
        if 'error' in param_dict:
            return jsonify(param_dict)

        cache_val = cache.get({param_dict['to']: param_dict['from']})
        if cache_val:
            return jsonify({
                'message': '',
                'error': 'sms from %s to %s blocked by STOP request' % (
                    param_dict['from'], param_dict['to'])
            })

        phone_number = models.PhoneNumber.query.filter(
            and_(models.PhoneNumber.number == param_dict['from'],
                 models.PhoneNumber.account_id == account.id)).first()

        if not phone_number:
            return jsonify({'message': '', 'error': 'from parameter not found'})

        from_val = cache.get(param_dict['from'])
        if from_val:
            from_val = cPickle.loads(from_val)
            if from_val['counter'] >= config.API_LIMIT:
                time_diff = (
                    datetime.utcnow() - from_val['timestamp']).total_seconds()
                if time_diff < config.COUNTER_RESET_TIME:
                    return jsonify({
                        'message': '',
                        'error': 'limit reached for from %s' % param_dict['from']
                    })
                else:
                    # Reset counter and timestamp
                    from_val['counter'] = 1
                    from_val['timestamp'] = datetime.utcnow()
                    cache.set(param_dict['from'], cPickle.dumps(from_val))
            else:
                # Increase counter
                from_val['counter'] += 1
                cache.set(param_dict['from'], cPickle.dumps(from_val))
        else:
            cache.set(
                param_dict['from'],
                cPickle.dumps(
                    {'counter': 1,
                     'timestamp': datetime.utcnow()
                     }))

        return jsonify({'message': 'outbound sms ok', 'error': ''})
    except Exception as ex:
        logging.info(ex)
        return jsonify({'message': '', 'error': 'unknown failure'})
