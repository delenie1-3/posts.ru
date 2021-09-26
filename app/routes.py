#-*- coding: utf-8 -*-
from app import app

'''@app.route('/')
@app.route('/index')
def index():
    return "Проверка работоспособности Flask"'''

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'web-dev'}
    return '''
    <html>
        <head>
            <title>Домашная страница - Posts</title>
        </head>
        <body>
            <h1>Приветствую, ''' + user['username'] + '''!</h1>
        </body>
    </html>
    '''