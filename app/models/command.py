from app import db

class Command(db.Model):
    __tablename__ = 'command'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    node_id = db.Column(db.String(10))
    sensor_type = db.Column(db.String(10))
    priority    = db.Column(db.String(10))
    command     = db.Column(db.String(10))
    real_time   = db.Column(db.String(80))

    def __init__(self, node_id, sensor_type,command,real_time='0', priority='1'):
        self.node_id = node_id
        self.sensor_type = sensor_type 
        self.command = command
        self.priority =  priority
        self.real_time = real_time

    def __repr__(self):
        return '<Node %r>' % self.node_id