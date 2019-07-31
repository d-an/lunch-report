from flask import Flask
import os

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Flask Dockerized ' + os.environ['user_key']

@app.route('/')
def show_menu():
    with open('lunch-report/lunch_report.html', 'rt') as f:
        menu = f.read()
    return menu

if __name__ == '__main__':
    app.run(host='0.0.0.0')
