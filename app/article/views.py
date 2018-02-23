#coding:utf8
from flask import render_template, session, redirect, url_for, current_app,flash,abort,request 
from flask_login import login_required, current_user
from .. import db
from ..models import User,Permission,Post,Role,Comment
from ..email import send_email
from . import article
from .forms import NameForm,PostForm,CommentForm
from ..decorators import admin_required,permission_required
from werkzeug import secure_filename

@article.route('/index',methods=['GET','POST'])
def index():
	form = PostForm()
	#分页
	page = request.args.get('page',1,type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page,per_page=20,error_out=False)
	posts = pagination.items
	return render_template('article/index.html',form=form,posts=posts,pagination=pagination)

@article.route('/list',methods=['GET','POST'])
def list():
	form = PostForm()

	#分页
	page = request.args.get('page',1,type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page,per_page=20,error_out=False)
	posts = pagination.items
	return render_template('article/article-list.html',form=form,posts=posts,pagination=pagination)

@article.route('/postArticle',methods=['GET','POST'])
def postArticle():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and \
			form.validate_on_submit():
		post = Post(title=form.title.data,
					body=form.body.data,
					author=current_user._get_current_object())
		db.session.add(post)
		#return redirect(url_for('article.postArticle'))
	return render_template('article/post_article.html',form=form)
#文章固定链接
@article.route('/cv<int:id>',methods=['GET','POST'])
def cv(id):
	post = Post.query.get_or_404(id)
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(body=form.body.data,
							post=post,
							author=current_user._get_current_object())
		db.session.add(comment)
		flash('Your comment has been published.')
		return redirect(url_for('.post',id=post.id,page=-1))
	page = request.args.get('page',1,type=int)
	if page == -1:
		page = (post.comments.count() - 1) / 20 + 1
	pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
		page,per_page=20,error_out=False)
	comments = pagination.items
	return render_template('post.html',posts=[post],form=form,
						comments=comments,pagination=pagination)
@article.route('/edit/cv<int:id>',methods=['GET','POST'])
@login_required
def editArticle(id):
	post = Post.query.get_or_404(id)
	if current_user !=post.author and \
			not current_user.can(Permission.ADMINISTER):
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title=form.title.data
		post.body = form.body.data
		db.session.add(post)
		flash("The post has been updated.")
	form.title.data = post.title
	form.body.data = post.body
	return render_template('edit_post.html',form=form,posts=[post])