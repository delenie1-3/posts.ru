#-*- coding: utf-8 -*-
from flask import render_template, flash, redirect, request, url_for
from app import app, login
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import Users
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse

'''@app.route('/')
@app.route('/index')
def index():
    return "Проверка работоспособности Flask"'''

@app.route('/')
@app.route('/index')
@login_required#декоратор для не аутентифицированных
def index():
    #user = {'username':'web-dev'}#проверочный пользователь(поддельный объект)
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
    return render_template('index.html', title='Домашняя страница', posts=posts)#главная страница

@app.route('/login', methods=['GET','POST'])#страница входа пользователя
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)#переход на страницу после авторизации
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():#функция выхода
    logout_user()
    return redirect(url_for('index'))