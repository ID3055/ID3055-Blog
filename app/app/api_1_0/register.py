# coding:utf-8
# 注册相关模块
from flask import current_app, g, jsonify, request, url_for

from . import api
from .. import db
from ..email import send_email
from ..models import Comment, Permission, Post, User
from .authentication import auth
from .decorators import confirmed_required, permission_required
from .errors import forbidden, unauthorized, bad_request


@api.route('/register', methods=['POST'])
# @auth.login_required
# @confirmed_required
def get_comment():
    if User.verify_user_exists(request.form.get('email')):
        return bad_request("this email is already exists")
    if User.verify_user_exists(request.form.get('username')):
        return bad_request("this username is already exists")
    try:
        user = User(email=request.form.get('email'),
                    username=request.form.get('username'),
                    password=request.form.get('password'))
        db.session.add(user)
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
               'auth/email/confirm', user=user, token=token)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(123)
        raise(e)
        

    return jsonify({"status": "success"})
