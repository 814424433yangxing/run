import threading
import queue
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_mqtt import Mqtt

from app.models.base_info import Base_info, base_info_primary
from app.CloudConn.proto_recv import proto_recv, Dict_Rsp
from app.CloudConn.proto_send import proto_send
import app.CloudConn.monitor_pb2 as proto
from app import mqtt, db
from app.control.count_thread import count_thread
from app.control.serial_thread import serial_thread
from app import scheduler
from app.models.sensor import Sensor_ID_map

proto_recv = proto_recv()
proto_send = proto_send()
data_queue = queue.Queue(10)

@mqtt.on_connect()
def handle_connect(client,userdata,flags,rc):
    scheduler.pause()
    db.drop_all()
    db.create_all()   
    base_info_primary()
    Sensor_ID_map()
    topic_subscribe=Base_info.query.filter_by(name='Topic_Subscribe').first().content
    mqtt.subscribe(topic_subscribe)
    threading.Thread(target=register_thread,args=()).start()

@mqtt.on_message()
def handle_mqtt_message(client,userdata,message):
    try:
        format = proto.ServerSend()
        format.ParseFromString(message.payload)
        name = format.WhichOneof("payload")
        result = Dict_Rsp[name](format)
        if result:
            data_queue.put(result)
    except:
        pass

def register_thread():
    mac = Base_info.query.filter_by(name = 'Mac').first().content
    register_info = proto_send.DRegisterReq(mac)
    mqtt.publish('register',register_info)
    while True:
        try:
            topic = data_queue.get(True,20)
            #get topic and update Base_info
            topic_subscribe = topic[0]
            topic_publish = topic[1]
            p = Base_info.query.filter_by(name = 'Topic_Publish').first()
            s = Base_info.query.filter_by(name = 'Topic_Subscribe').first()
            p.content = topic_publish
            s.content = topic_subscribe
            db.session.add_all([p,s])
            db.session.commit()
            #unsubscribe 
            mqtt.unsubscribe_all()
            mqtt.subscribe(topic_subscribe)
            data_queue.queue.clear()
            threading.Thread(target=query_thread,args=()).start()
            break
        except:
            mqtt.publish('register',register_info)

def heartbeat_thread():
    heartbeat = proto_send.Heartbeat()
    topic_publish = Base_info.query.filter_by(name = 'Topic_Publish').first().content
    mqtt.publish(topic_publish,heartbeat)

def query_thread():
    queryCycle_info = proto_send.DQueryCycleReq()
    topic_publish = Base_info.query.filter_by(name = 'Topic_Publish').first().content
    mqtt.publish(topic_publish,queryCycle_info)
    while True:
        try:
        #???//???
            data_queue.get(True,20)
            data_queue.queue.clear()
            cyclesetrsp_info = proto_send.DcycleSetRsp()
            mqtt.publish(topic_publish,cyclesetrsp_info)
            scheduler.resume()
            break
        except:
            mqtt.publish(topic_publish,queryCycle_info)


def Scheduler():
    scheduler.add_job(func = heartbeat_thread,args=(),trigger='interval',seconds=120,id='heartbeat_thread')
    scheduler.add_job(func = count_thread,args=(),trigger='interval',seconds=1,id='count_thread')
    scheduler.add_job(func = serial_thread,args=(),next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=5),id='serial_thread')
    scheduler.start()
