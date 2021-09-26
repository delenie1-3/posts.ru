from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Проверка работоспособности Flask"