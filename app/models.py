from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hesh

class Users(db.Model):#Модель(таблица) пользователя
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Posts', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):#создание хэша пороля
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):#проверка хеша с поролем
        return check_password_hesh(self.password_hash, password)

class Posts(db.Model):#Модель(таблица) постов
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.Integer, index=True, default=datetime.utcnow) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)