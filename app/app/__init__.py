#coding: utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

from config import config

# 实例化各个flask扩展模块
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'string'
# 需要注册时跳转的view
login_manager.login_view = 'auth.login'

#应用工厂函数
def create_app(config_name):
    app = Flask(__name__)

    #load config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化各个flask扩展模块
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)

    # 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    
    from .article import article as article_blueprint
    app.register_blueprint(article_blueprint,url_prefix='/article')
    
    # from .spider import spider as spider_blueprint
    # app.register_blueprint(spider_blueprint,url_prefix='/spider')

    from .manage import manage as manage_blueprint
    app.register_blueprint(manage_blueprint,url_prefix='/manage')
    
    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint,url_prefix='/api/v1.0')

    return app
