from app import db

class Sensor(db.Model):
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    sensor_cloud = db.Column(db.Integer)
    sensor_name = db.Column(db.String(10))
    sensor_LAN    = db.Column(db.String(10))
   
    
    def __init__(self, sensor_cloud, sensor_name,sensor_LAN):
        self.sensor_cloud = sensor_cloud
        self.sensor_name = sensor_name 
        self.sensor_LAN = sensor_LAN
       

    def __repr__(self):
        return '<Sensor %r>' % self.sensor_name

def Sensor_ID_map():
    a = Sensor(1,'A_T','10')
    b = Sensor(2,'A_H','11')
    c = Sensor(3,'A_P','12')
    d = Sensor(4,'S_T','20')
    e = Sensor(5,'S_H','21')
    f = Sensor(6,'A_L','13')
    g = Sensor(7,'/','/')
    h = Sensor(8,'/','/')
    i = Sensor(9,'/','/')
    j = Sensor(10,'Bat_AD','41')
    k = Sensor(11,'Sun_AD','42')
    l = Sensor(12,'W_S','15')
    m = Sensor(13,'W_D','16')
    db.session.add_all([a,b,c,d,e,f,g,h,i,j,k,l,m])
    db.session.commit()