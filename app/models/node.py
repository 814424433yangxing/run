from app import db

class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    node_id = db.Column(db.String(10))
    channel = db.Column(db.String(10))
    description = db.Column(db.String(80))
    query_time = db.relationship('Query',backref='node')
    
    def __init__(self,node_id,channel,description='/'):
        self.node_id = node_id
        self.channel = channel
        self.description = description
       
    def __repr__(self):
        return '<Node %r>' % self.node_id

class Query(db.Model):
    __tablename__ = 'query_time'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    sensor_type = db.Column(db.String(10),)
    query_time = db.Column(db.String(10))
    node_id = db.Column(db.String(10),db.ForeignKey('node.id'))
    
    def __init__(self,sensor_type,query_time,node_id):
        self.sensor_type = sensor_type 
        self.query_time = query_time
        self.node_id = node_id
       
    def __repr__(self):
        return '<Query %r>' % self.sensor_type