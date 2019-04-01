# coding: utf-8
# 账户权限验证模块，作用域限于api蓝图中

from functools import wraps
from flask import g
from .errors import forbidden

#需要传参的写法
#账号权限
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator

#不需要传参的写法
#账号已邮件验证
def confirmed_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.current_user.is_anonymous and not g.current_user.confirmed:
            return forbidden('Unconfirmed account')
        return f(*args, **kwargs)
    return decorated_function
