# coding: utf-8
# 此蓝图中的error处理
from flask import jsonify

from . import api
from ..exceptions import ValidationError


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response
    

def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

#errorhandler用法
#注册一个在蓝图中生效的函数，用来处理特定类型错误,app全局生效的要用app_errorhandler

#处理异常
#如何触发：
#from ..exceptions import ValidationError
#raise ValidationError('xxxxxxx')

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
