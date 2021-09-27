from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)#основное приложение
app.config.from_object(Config)

db = SQLAlchemy(app)#БД
migrate = Migrate(app, db)



from app import routes, models