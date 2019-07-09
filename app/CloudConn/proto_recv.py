from app.CloudConn.analysis_C import analysis_C
import app.CloudConn.monitor_pb2 as proto
from app import db
from app.models.node import Node,Query
from app.models.command import Command
from app.models.serial_command import Serial
from app.models.base_info import Base_info
from app.models.sensor import Sensor

class proto_recv():
	def SRegisterRsp(self,format):
		RegisterId = int(Base_info.query.filter_by(name = 'RegisterId').first().content)
		if format.sid == RegisterId:
			Topic_Subscribe = format.register.scribeTopic
			Topic_Publish = format.register.sendTopic
			return [Topic_Subscribe,Topic_Publish]
		else:
			return False
		
	def SCycleSetReq(self,format):
		c = Base_info('CycleSetId',str(format.sid))
		db.session.add(c)
		db.session.commit()
		cycleset = format.cycleSet
		Gate_ID = '0002'
		cmd_data = '00'
		if True:
			for cycle in cycleset.cycle:
				ID = str(cycle.node.address).zfill(4)
				Channel = str(cycle.node.channel).zfill(2)
				#Gate_info = Gate_ID + Channel
				Gate_info = Gate_ID + "09"
				Node_info = ID + Channel
				node = Node(ID,Channel)
				db.session.add(node)
				db.session.commit()
				for index in cycle.cycle:
					if True:
						#此处可以建表传感器类型对应表
						sensor_Lan = Sensor.query.filter_by(sensor_cloud = index.sensor).first().sensor_LAN
						CMD_list = analysis_C().Build_CMD(Node_info,Gate_info,sensor_Lan,cmd_data,index.interval)
						sensor_type = CMD_list[1]			
						cmd = Command(ID,sensor_type,CMD_list[0],index.interval)
						db.session.add(cmd)
						db.session.commit()
						
						query = Query(sensor_type,index.interval,ID)
						db.session.add(query)
						db.session.commit()
						cmd = Serial(ID,sensor_type,CMD_list[0],'1')
						db.session.add(cmd)
						db.session.commit()
			return True
		
	def SSensorCtrlReq(self,format):
		try:
			row = self.dict()
			self.SensorCtrlId = format.sid
			sensorctrl = format.sensorCtrl
			ID = str(sensorctrl.node.address).zfill(2)
			sensor = sensorctrl.sensor
			ctrlcmd = sensorctrl.cmd
			if sensor == 8:
				if ctrlcmd == 2:
					data_init = ID + "060362FF08"
					data = data_init + crc.crc_modbus(self,data_init)
					self.data_ctrl.put([data,'FF'])
				elif ctrlcmd == 3:
					data_init = ID + "0603620008"
					data = data_init + crc.crc_modbus(self,data_init)
					self.data_ctrl.put([data,'FF'])
				elif ctrlcmd == 4:
					format = proto.AirConditioningParams()
					format.ParseFromString(sensorctrl.params)
					mode = format.mode
					temp = format.temperature
					if mode!=self.mode:
						data_init = ID + "060364" + hex(mode)[2:4] + "08"
						data = data_init + crc.crc_modbus(self,data_init)
						self.data_ctrl.put([data,'FF'])
					if temp!=self.temp:
						data_init = ID + "060366" + hex(temp)[2:4] + "08"
						data = data_init + crc.crc_modbus(self,data_init)
						self.data_ctrl.put([data,'FF'])
			elif sensor == 9:
				if ctrlcmd == 2:
					data_init = ID + "050003FFFF"
					data = data_init + crc.crc_modbus(self,data_init)
					self.data_ctrl.put([data,'FF'])
				elif ctrlcmd == 3:
					data_init = ID + "0500040000"
					data = data_init + crc.crc_modbus(self,data_init)
					self.data_ctrl.put([data,'FF'])
			else:
				if ctrlcmd == 1:
					Sensor_Name = self.Dict_Sensor_Name[sensor]
					cmd = analysis_C.Build_CMD_ctrl(self,ID,row[Sensor_Name])
					cmd.append(sensor)
					self.data_ctrl.put(cmd)
		except:
			pass
		finally:
			return False
			
	def Heartbeat(self,format):
		HeartbeatID = Base_info.query.filter_by(name='HeartbeatId').first().content
		if format.sid == int(HeartbeatID):
			print("Heartbeat_Rsp")
		return False
	
	def SQueryNodeRsp(self,format):
		print("ServerRsp")
		
	def SQueryCycleRsp(self,format):
		pass
		
	def SNodeManageReq(self,format):
		pass
		
	def SSensorValueRsp(self,format):
		pass


Dict_Rsp = {\
	"register" : proto_recv().SRegisterRsp,\
	"cycleSet" : proto_recv().SCycleSetReq,\
	"sensorCtrl" : proto_recv().SSensorCtrlReq,\
	"heartbeat" : proto_recv().Heartbeat,\
	"sensorValue" : proto_recv().SSensorValueRsp,\
	"queryCycle" : proto_recv().SQueryCycleRsp\
}

