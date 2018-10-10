from flask import Flask,request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler,RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap 
from flask_moment import Moment
from flask_babel import Babel


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' 
login_manager.session_protection = 'strong'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
# http://www.unicode.org/cldr/charts/latest/supplemental/territory_language_information.html
babel = Babel()

def create_app():
    
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    app.config.from_object(Config)
    from app.errors import errors_bp
    app.register_blueprint(errors_bp)
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.userop import user_bp
    app.register_blueprint(user_bp)
    from app.main import main_bp
    app.register_blueprint(main_bp)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    # 相关的东西需要引入进来，实际就是一个单文件
    from app import routes,models
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
        
    
    return app

