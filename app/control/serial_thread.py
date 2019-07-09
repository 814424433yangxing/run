from app.models.serial_command import Serial
from app import db,mqtt
import time
import threading
from app.control.serial_config import Ser
from app.models.recv_data import Data
from app.models.base_info import Base_info
from app.CloudConn.analysis_D import Dict_Sensor

def serial_thread():  
    ser = Ser()
    while True:
        index = Serial.query.first()
        if index:
            cmd = index.command
            print('send: ' + cmd)
            cmd = bytes().fromhex(cmd)
            ser.write(cmd)
            count = 20
            while count > 0:
                ser_receive = ser.receive()
                if ser_receive:
                    print('recv: ' + ser_receive)
                    try:
                        sensor_type = ser_receive[6:8]
                        result = Dict_Sensor[sensor_type](ser_receive,sensor_type)
                        topic_publish = Base_info.query.filter_by(name = 'Topic_Publish').first().content
                        mqtt.publish(topic_publish,result)
                        '''
                        recv_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                        date_len = int(ser_receive[8:10])
                        recv_data = ser_receive[10:10+2*date_len]
                        d = Data(node_id,sensor_type,recv_time,recv_data)
                        db.session.add(d)
                        db.session.commit()
                        '''
                        break
                    except:
                        pass
                count -= 1
                time.sleep(1)
            db.session.delete(index)
            db.session.commit()