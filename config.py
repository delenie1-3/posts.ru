import os

class Config(object):#класс конфигурации приложения
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'