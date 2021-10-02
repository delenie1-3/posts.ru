from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import app, login
from hashlib import md5
from time import time
import jwt

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
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

    #функциональности подписки/отписки/отношение
    def follow(self, user):#подписка на пользователя
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):#отписка от пользователя
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):#отношение подписки
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):#запрос на получение всех постов на которые подписан и своих
        followed = Posts.query.join(
            followers, (followers.c.followed_id == Posts.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Posts.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Posts.timestamp.desc())
        '''return Posts.query.join(
            followers, (followers.c.followed_id == Posts.user_id).filter(
                followers.c.follower_id == self.id).order_by(Posts.timestamp.desc())
        )'''#без своих постов

    def get_reset_password_token(self, expires_in=600):#генерация токена
        return jwt.encode(
            {'reset_password':self.id, 'exp':time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):#верификация токена
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return Users.query.get(id)

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
