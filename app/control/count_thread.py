from app.models.command import Command
from app.models.node import Query
from app.models.serial_command import Serial
from app import  db
import time


def count_thread():
    for index in Command.query.all():
        real_time = int(index.real_time) - 1
        if real_time <= 0:
            real_time = int(Query.query.filter_by(node_id=index.node_id,sensor_type=index.sensor_type).first().query_time)
            s = Serial(index.node_id,index.sensor_type,index.command,index.priority)
            db.session.add(s)
            db.session.commit()
        #update command query time
        index.real_time = str(real_time)
        db.session.add(index)
        db.session.commit()
