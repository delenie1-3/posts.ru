from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user_id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user_id'))
)#вспомогательная таблица для подписчиков

class Users(UserMixin, db.Model):#Модель(таблица) пользователя и входа
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Posts', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)



    followed = db.relationship(
        'Users', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):#создание хэша пороля
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):#проверка хеша с поролем
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):#метод получения аватарки пользователя с gravatar
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Posts(db.Model):#Модель(таблица) постов
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.Integer, index=True, default=datetime.utcnow) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):#загрузчик пользлвательского id
    return Users.query.get(int(id))
