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


@api.route('/post/<int:id>')
@auth.login_required
@confirmed_required
def post(id):
    #get_or_404()是主键查询，比get()多了404的功能
    post = Post.query.get_or_404(id)
    print(post)
    return jsonify({"status": "success", "post": post})