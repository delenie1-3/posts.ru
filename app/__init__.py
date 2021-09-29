from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)#основное приложение
app.config.from_object(Config)#приложение конфигурации

db = SQLAlchemy(app)#БД
migrate = Migrate(app, db)#миграция БД

login = LoginManager(app)#приложение логин
login.login_view = 'login'#перенаправление на ввод логина



from app import routes, models, errors