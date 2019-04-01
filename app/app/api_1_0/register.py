# coding:utf-8
# 注册相关模块
from flask import current_app, g, jsonify, request, url_for

from . import api
from .. import db
from ..models import Comment, Permission, Post
from .decorators import permission_required, confirmed_required

from .authentication import auth

@api.route('/register', methods=['POST'])
@auth.login_required
@confirmed_required
def get_comment():
    return jsonify({"status": "success"})
