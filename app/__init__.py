import os
import threading
import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt
from flask_apscheduler import APScheduler

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
mqtt = Mqtt()
scheduler = APScheduler()  
app = Flask(__name__)


def mqtt_thread():
    while True:
        try:
            mqtt.init_app(app)
            print("MQTT连接成功")
            break
        except:
            print('MQTT连接失败')
            time.sleep(2)

def create_app():

    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.config['MQTT_BROKER_URL'] = '47.104.97.199'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 60
    app.config['MQTT_TLS_ENABLED'] = False
    
    db.init_app(app)
    db.app = app

    from app.base import Scheduler
    scheduler.init_app(app)
    Scheduler()
    time.sleep(1)
    
    threading.Thread(target=mqtt_thread,args=()).start()

    return app
    