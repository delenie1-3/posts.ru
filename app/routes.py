#-*- coding: utf-8 -*-
from flask import render_template, flash, redirect
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

@app.route('/login', methods=['GET','POST'])#страница входа пользователя
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, rememeber_me={}'.format(
            form.username.data.data, form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)