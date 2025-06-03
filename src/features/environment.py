from database import db
from app import app
from models.pessoa import Pessoa

def before_scenario(context, scenario):
    with app.app_context():
        db.drop_all()
        db.create_all()
