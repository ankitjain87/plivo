from flask import Blueprint

import views

mod = Blueprint('app', __name__)

mod.add_url_rule('/', view_func=views.index, methods=['GET'])
mod.add_url_rule(
    '/inbound/sms/', view_func=views.inbound, methods=['POST'])
mod.add_url_rule(
    '/outbound/sms/', view_func=views.outbound, methods=['POST'])