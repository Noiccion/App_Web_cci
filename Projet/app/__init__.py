from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='/home/lucas/Documents/project/app/templates', static_url_path='/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    
    db.init_app(app)

    
    from . import routes

    return app
