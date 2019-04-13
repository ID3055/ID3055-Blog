# coding: utf-8
#!/usr/bin/env python
# Author: ID3055
import hashlib
from datetime import *

import bleach
from flask import current_app, url_for
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


class Permission:
    '''
    具体的权限
    '''
    FOLLOW = 0x01#关注
    COMMENT = 0x02#评论
    WRITE_ARTICLES = 0x04#发表文章
    MODERATE_COMMENTS = 0x08#管理评论
    ADMINISTER = 0x80#admin

class Role(db.Model):
    #定义表名
    __tablename__ = 'roles'
    #定义列
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 如果role的default为True，用户注册时会默认选这一种role
    default = db.Column(db.Boolean,default=False,index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
        'User':(Permission.FOLLOW|
                Permission.COMMENT|
                Permission.WRITE_ARTICLES,True),
        'Moderateor':(Permission.FOLLOW|
                      Permission.COMMENT|
                      Permission.WRITE_ARTICLES|
                      Permission.MODERATE_COMMENTS,False),
        'Administrator':(0xff,False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    #是否已经通过邮件验证
    confirmed = db.Column(db.Boolean, default=False)

    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(),default=datetime.utcnow)#注册
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)#最后访问

    avatar_hash = db.Column(db.String(32))#头像hash

    posts = db.relationship('Post', backref='author', lazy='dynamic')#文章
    status = db.relationship('Statue', backref='author', lazy='dynamic')#状态
    comments = db.relationship('Comment',backref='author',lazy='dynamic')
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    @staticmethod
    def verify_user_exists(email):
        return User.query.filter_by(email=email).first() is not None

    def verify_username_exists(username):
        return User.query.filter_by(username=username).first() is not None

    def generate_confirmation_token(self, expiration=3600):
        # 将{'confirm': self.id}加密生成token
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'reset':self.id})

    def reset_password(self,token,new_password):
        s= Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') !=self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True
    
    def can(self,permissions):
        '''
        确认是否拥有permissions所指定的权限
        '''
        return self.role is not None and (self.role.permissions & permissions)==permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
        
    def ping(self):#刷新最后访问时间
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def getavatar(self,size=100):
        '''
        avatar头像
        '''
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        url = url_for('static', filename='avatar/{hash}.jpg'.format(hash=hash))
        return url
    
    def generate_auth_token(self, expiration):
        '''
        生成api token
        '''
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        '''
        验证token
        '''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    @staticmethod
    def generate_fake(count=100):
        '''
        生成测试用的条目
        '''
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                        username=forgery_py.internet.user_name(True),
                        password=forgery_py.lorem_ipsum.word(),
                        role_id=2,
                        confirmed=True,
                        name=forgery_py.name.full_name(),
                        location=forgery_py.address.city(),
                        about_me=forgery_py.lorem_ipsum.sentence(),
                        member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class AnnoymousUser(AnonymousUserMixin):#匿名用户
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False


class Post(db.Model):
    '''
    文章
    '''
    #表名
    __tablename__ = 'posts'
    #定义字段
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)#用户输入的原文
    body_html = db.Column(db.Text)#用户原文经过安全过滤输出的html
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment',backref='post',lazy='dynamic')
     
    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p','br','strike']#允许存储的标签，要实现富文本必须先补全这个
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value,output_format='html'),
            tags=allowed_tags,strip=True))

    @staticmethod
    def generate_fake(count=100):
        from random import seed,randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(title=forgery_py.lorem_ipsum.title(),
                    body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                    timestamp=forgery_py.date.date(True),
                    author=u)
            db.session.add(p)
            db.session.commit()


class Statue(db.Model):
    '''
    个人签名
    '''
    #表名
    __tablename__ = 'statues'
    #定义字段
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value,output_format='html'),
            tags=allowed_tags,strip=True))

    @staticmethod
    def generate_fake(count=100):
        from random import seed,randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            s = Status(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                    timestamp=forgery_py.date.date(True),
                    author=u)
            db.session.add(s)
            db.session.commit()


class Comment(db.Model):
    '''
    评论
    '''
    #表名
    __tablename__ = 'comments'
    #定义字段
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

#当字段内容有变动时，先调用静态方法预处理
db.event.listen(Post.body,'set',Post.on_changed_body)
db.event.listen(Statue.body,'set',Statue.on_changed_body)
db.event.listen(Comment.body, 'set', Comment.on_changed_body)

#匿名用户
login_manager.anonymous_user = AnnoymousUser


#flask-login加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
