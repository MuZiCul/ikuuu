from flask import Flask
from flask_apscheduler import APScheduler

from job import sign_in_iku

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@scheduler.task('cron', id='iku', hour=1)
def sign_In():
    sign_in_iku()


if __name__ == '__main__':
    from gevent import pywsgi

    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
