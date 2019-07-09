import app.CloudConn.monitor_pb2 as proto
import time
from app.models.base_info import Base_info
from app.models.command import Command
from app.models.node import Node
from app import db

Dict_server = {\
	'10':1,\
	'11':2,\
	'12':3,\
	'20':4,\
	'21':5,\
	'13':6,\
	'41':10,\
	'42':11,\
	'14':12,\
	'15':13\
}
class proto_send():
	def DRegisterReq(self,mac):
		format = proto.GateSend()
		sid = Base_info.query.filter_by(name = 'sid').first()
		RegisterId = sid.content
		sid.content = str(int(sid.content) + 1)

		r = Base_info.query.filter_by(name = 'RegisterId').first()
		r.content = RegisterId

		db.session.add_all([sid,r])
		db.session.commit()

		format.sid = int(RegisterId)
		payload = format.register
		payload.macId = mac
		return format.SerializeToString()
	
	def DcycleSetRsp(self):
		format = proto.GateSend()
		CycleSetId = Base_info.query.filter_by(name = 'CycleSetId').first().content
		format.sid = int(CycleSetId)
		payload = format.cycleSet
		payload.errorcode = 0
		return format.SerializeToString()
	
	def DSensorCtrlRsp(self,errorcode,IP,value1,value2,sensor):
		format = proto.GateSend()
		format.sid = self.SensorCtrlId
		payload = format.sensorCtrl
		payload.errorcode = errorcode
		value = payload.value
		node = value.node
		try:
			node.nodeId = self.Dict[IP][2]
			node.sensors.extend(self.Dict[IP][0])
			node.address = int(IP)
			node.channel = int(self.Dict[IP][1])
			value.sensor = sensor
			value.value1 = value1
			value.value2 = value2
		except:
			pass
		return format.SerializeToString()
	
	def Heartbeat(self):
		format = proto.GateSend()
		sid = Base_info.query.filter_by(name = 'sid').first()
		HeartbeatId = sid.content
		sid.content = str(int(sid.content) + 1)
		db.session.add(sid)
		db.session.commit()
		format.sid = int(HeartbeatId)
		payload = format.heartbeat
		payload.time = int(time.time())
		return format.SerializeToString()
		
	def SensorValue(self,ID,sensor,value1,value2):
		format = proto.GateSend()
		sid = Base_info.query.filter_by(name = 'sid').first()
		SensorValueId = sid.content
		RegisterId = sid.content
		sid.content = str(int(sid.content) + 1)

		r = Base_info.query.filter_by(name = 'RegisterId').first()
		r.content = RegisterId


		db.session.add_all([sid,r])
		db.session.commit()
		format.sid = int(SensorValueId)
		payload = format.sensorValue
		node = payload.node
		node.nodeId = int(ID)
		sensor_list = []
		ID = '0003'
		sensor1 = Command.query.filter_by(node_id = ID).all()

		for index in sensor1:
			sensor_list.append(Dict_server[index.sensor_type])
			
		node.sensors.extend(sensor_list)
		node.address = int(ID)
		channel = Node.query.filter_by(node_id = ID).first().channel
		node.channel = int(channel)
		payload.sensor = sensor
		payload.value1 = value1
		payload.value2 = value2
		return format.SerializeToString()
		
	def DQueryNodeReq(self):
		pass
		
	def DQueryCycleReq(self):
		format = proto.GateSend()
		sid = Base_info.query.filter_by(name = 'sid').first()
		QueryCycleId = sid.content
		sid.content = str(int(sid.content) + 1)
		q = Base_info('QueryCycleId',QueryCycleId)
		db.session.add_all([sid,q])
		db.session.commit()
		format.sid = int(QueryCycleId)
		payload = format.queryCycle
		payload.timestamp = int(time.time())
		return format.SerializeToString()
		
	def DNodeManageRsp(self):
		pass