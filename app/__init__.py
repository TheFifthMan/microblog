from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler,RotatingFileHandler
import os
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.session_protection = 'strong'
mail = Mail(app)


# 相关的东西需要引入进来，实际就是一个单文件
from app import routes,models,errors
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_SSL']:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost=app.config['MAIL_SERVER'],
            fromaddr=app.config['MAIL_USERNAME'],
            toaddrs=app.config['ADMINS'],
            subject="Microblog Error",
            credentials=auth,secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler('logs/microblog.log',maxBytes=10240,backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('Microblog start.')

