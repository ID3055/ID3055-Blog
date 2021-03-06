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

class EditProfileForm(FlaskForm):
    name = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('submit')

class EditAvatarForm(FlaskForm):
    #avatar = FileField('Your Avatar')
    avatar = FileField('Your Avatar', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    username = StringField('Username',validators=[
        Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                        'Usernames must have only letters, '
                                        'numbers, dots or underscores')])
    confirmed = BooleanField('Comfirmed')
    role = SelectField('Role',coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name)
                            for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self,field):
        if field.data != self.user.email and \
                user.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class CommentForm(FlaskForm):
    body = StringField('',validators=[Required()])
    submit = SubmitField('submit')
        