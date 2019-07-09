from app import db

class Serial(db.Model):
    __tablename__ = 'serial'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    node_id = db.Column(db.String(10))
    sensor_type = db.Column(db.String(10))
    priority    = db.Column(db.String(10))
    command     = db.Column(db.String(80))
    
    def __init__(self, node_id, sensor_type,command, priority):
        self.node_id = node_id
        self.sensor_type = sensor_type 
        self.command = command
        self.priority =  priority
 

    def __repr__(self):
        return '<Node %r>' % self.node_id