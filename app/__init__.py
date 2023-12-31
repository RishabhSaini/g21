# app/__init__.py
import sqlalchemy as sa
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_wtf.csrf import CSRFProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info("Initialized database")
    else:   
        app.logger.info("Database already contains user table.")
    
    login_manager.login_view = "main.login"
    login_manager.init_app(app)

    from .main import main as main_blueprint
    from .main.events import events_blueprint
    from .main.organizers import organizers_blueprint
    from .main.users import users_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(organizers_blueprint)
    app.register_blueprint(events_blueprint)
    

    return app
