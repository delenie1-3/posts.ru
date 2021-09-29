from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import Users

class LoginForm(FlaskForm):#форма входа пользователя
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Отправить')

class RegistrationForm(FlaskForm):#Форма регистрации
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):#проверка имени пользователя в БД
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста используйте другое имя пользователя.')
    
    def validate_email(self, email):#проверка email в БД
        user_email = Users.query.filter_by(email=email.data).first()
        if user_email is not None:
            raise ValidationError('Пожалуйста используйте другой email')

class EditProfileForm(FlaskForm):#форма редактирования данных пользователя
    username = StringField('Имя пользователя', validators=[DataRequired()])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=140)])
    submit = SubmitField('Изменить')