from app import db
import uuid


class Base_info(db.Model):
    __tablename__ = 'base_info'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    name = db.Column(db.String(80))
    content = db.Column(db.String(80))
    def __init__(self,name,content):
        self.name = name
        self.content = content

    def __repr__(self):
        return '<Base_info %r>' % self.name

def base_info_primary():
    #local_mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    #local_mac = ":".join([local_mac[e:e+2] for e in range(0,11,2)]) #去掉冒号后
    #topic_subscribe = local_mac
    topic_subscribe = "b827ebcec317" #测试用
    topic_publish = 'register'
    mac = ":".join([topic_subscribe[e:e+2] for e in range(0,11,2)])
    m = Base_info('Mac',mac)
    s = Base_info('Topic_Subscribe',topic_subscribe)
    p = Base_info('Topic_Publish',topic_publish)
    sid = Base_info('sid','0')
    RegisterId = Base_info('RegisterId','/')
    db.session.add_all([m,p,s,sid,RegisterId])
    db.session.commit()


