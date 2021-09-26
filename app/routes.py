#-*- coding: utf-8 -*-
from flask import render_template
from app import app
from app.forms import LoginForm

'''@app.route('/')
@app.route('/index')
def index():
    return "Проверка работоспособности Flask"'''

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'web-dev'}#проверочный пользователь(поддельный объект)
    posts = [
        {
            'author':{'username':'Саша'},
            'body':'Сообщение от Саши!'
        },
        {
            'author':{'username':'Даша'},
            'body':'Сообщение от Даши!'
        },
        {
            'author':{'username':'Наташа'},
            'body':'Сообщение от Наташи!'
        }
    ]
    return render_template('index.html', title='Домашняя страница', user=user, posts=posts)#главная страница

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Вход', form=form)