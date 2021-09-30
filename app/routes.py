#-*- coding: utf-8 -*-
from flask import render_template, flash, redirect, request, url_for
from app import app, login, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from flask_login import current_user, login_user
from app.models import Users, Posts
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime


'''@app.route('/')
@app.route('/index')
def index():
    return "Проверка работоспособности Flask"'''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required#декоратор для не аутентифицированных
def index():
    #user = {'username':'web-dev'}#проверочный пользователь(поддельный объект)
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Постик в эфире!')
        return redirect(url_for('index'))
    posts = [
        {
            'author': {'username':'user1'},
            'body': 'Проверочное сообщение от user1'
        },
        {
            'author': {'username':'user2'},
            'body': 'Проверочное сообщение от user2'
        }
    ]
    return render_template('index.html', title='Домашняя страница', form=form, posts=posts)#главная страница

@app.route('/login', methods=['GET','POST'])#страница входа пользователя
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #flash('Зайдите в свой аакаунт для доступа к этой странице')
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

@app.route('/register', methods=['GET', 'POST'])
def register():#функция обработки регистрации
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляю, вы зарегистрировались!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/user/<username>')
@login_required
def user(username):#функция страницы пользователя
    user = Users.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user, 'body':'Test post1'},
        {'author':user, 'body':'Test post2'},
    ]
    return render_template('user.html', title='Профиль пользователя', user=user, posts=posts)

@app.before_request
def before_request():#Функция записи последнего посещения пользователя
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():#функция правки полелй пользователя
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения сохранены!')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Изменение профиля', form=form)

@app.route('/follow/<username>')#подписка на посты пользователя
@login_required
def follow(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        flash('Пользователь {} не найден.'.fromat(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('Вы не можете подписаться на самого себя')
        return redirect(url_for('user', username))
    current_user.follow(user)
    db.session.commit()
    flash('Вы подписаны на {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):#отписка от постов пользователя
    user = Users.query.filter_by(username=username).first()
    if user is None:
        flash('Пользователь {} не найден.'.fromat(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('Вы не можете подписаться на самого себя')
        return redirect(url_for('user', username))
    current_user.unfollow(user)
    db.session.commit()
    flash('Вы отписаны от {}!'.format(username))
    return redirect(url_for('user', username=username))

