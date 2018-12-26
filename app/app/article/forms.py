#coding:utf8
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from ..models import Role,User
from flask_pagedown.fields import PageDownField

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('title', validators=[Required()])
    body = TextAreaField("write something",validators=[Required()])
    submit = SubmitField('submit')

class CommentForm(FlaskForm):
    body = StringField('',validators=[Required()])
    submit = SubmitField('submit')
        