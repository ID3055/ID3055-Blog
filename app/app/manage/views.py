#coding:utf8
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import manage
from .. import db
from ..decorators import admin_required,permission_required
from ..models import User,Permission,Post,Role,Comment

@manage.route('/',methods=['GET','POST'])
@login_required
@permission_required(Permission.ADMINISTER)
def index():
    return render_template('manage/index.html')

# @manage.route('/moderate/disable/<int:id>')
# @login_required
# @permission_required(Permission.MODERATE_COMMENTS)
# def moderate_disable(id):
#     comment = Comment.query.get_or_404(id)
#     comment.disabled = True
#     db.session.add(comment)
#     return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))

