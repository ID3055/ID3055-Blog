# coding:utf-8
# 用户验证身份模块
from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth

from . import api
from ..models import User
from .errors import forbidden, unauthorized
from .decorators import confirmed_required

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


#注册HTTPBasicAuth的error_handler, 用于处理身份验证error 
@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


# 注册一个验证函数，在此蓝图中生效
# @api.before_request
# @auth.login_required
# def before_request():
#     if not g.current_user.is_anonymous and not g.current_user.confirmed:
#         return forbidden('Unconfirmed account')


@api.route('/token', methods=['POST', 'GET'])
@auth.login_required
@confirmed_required
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalida credentials')
    return jsonify({
        'token': g.current_user.generate_auth_token(expiration=3600), 
        'expiration': 3600})

