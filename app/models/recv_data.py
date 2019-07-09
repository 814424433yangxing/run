from app import db

class Data(db.Model):
    __tablename__ = 'recv_data'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    node_id = db.Column(db.String(10))
    sensor_type = db.Column(db.String(10))
    time = db.Column(db.String(80))
    recv_data = db.Column(db.String(10))

    def __init__(self, node_id, sensor_type,time,recv_data):
        self.node_id = node_id
        self.sensor_type = sensor_type 
        self.time = time
        self.recv_data = recv_data
    def __repr__(self):
        return '<Node %r>' % self.address