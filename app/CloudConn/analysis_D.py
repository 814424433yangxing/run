from app.CloudConn.proto_send import proto_send
from app.models.recv_data import Data
from app import db
import time

class analysis_D():
	def W_S(self,data,check,sensor=0):
		#W_S		12
		node_id = data[0:4]
		sensor_type = data[6:8]
		recv_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		data_len = 1
		recv_data = data[8:8+2*data_len]
		d = Data(node_id,sensor_type,recv_time,recv_data)
		db.session.add(d)
		db.session.commit()
		'''
		Date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		IP = data[0:2]
		WS_DATA = int(data[6:10],16)/10
		Data = str(int(data[6:10],16)/10) + ' m/s'
		if len(check) == 6:
			print('ctrl')
			ws_data = proto_send.DSensorCtrlRsp(self,0,data[0:2],WS_DATA,0,sensor)
		else:
			ws_data = proto_send.SensorValue(self,IP,3,WS_DATA,0)
		sql = "INSERT INTO W_S(Date,IP,Data)\
					VALUES ('%s','%s','%s')" % (Date,IP,Data)
		try:
			database.commit_D(self,sql)
		except:
			pass
		return ws_data
		'''
		
	def W_D(self,data,check,sensor=0):
		#W_D		13
		node_id = data[0:4]
		sensor_type = data[6:8]
		recv_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		data_len = 1
		recv_data = data[8:8+2*data_len]
		d = Data(node_id,sensor_type,recv_time,recv_data)
		db.session.add(d)
		db.session.commit()
		'''
		Date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		IP = data[0:2]
		Data = 360 - int(data[6:10],16)/10
		WD_DATA = Data
		if Data == 0.0:
			Data = "North " + str(Data)
		elif 0.0 < Data < 90.0:
			Data = "Northwest " + str(Data)
		elif Data == 90.0:
			Data = "West " + str(Data)
		elif 90.0 < Data < 180.0:
			Data = "Southwest " + str(Data)
		elif Data == 180.0:
			Data = "South " + str(Data)
		elif 180.0 < Data < 270.0:
			Data = "Southwest " + str(Data)
		elif Data == 270.0:
			Data = "East " + str(Data)
		elif 270.0 < Data < 360.0:
			Data = "Northeast " + str(Data)
		if len(check) == 6:
			print('ctrl')
			wd_data = proto_send.DSensorCtrlRsp(self,0,data[0:2],WD_DATA,0,sensor)
		else:
			wd_data = proto_send.SensorValue(self,IP,13,WD_DATA,0)
		sql = "INSERT INTO W_S(Date,IP,Data)\
					VALUES ('%s','%s','%s')" % (Date,IP,Data)
		try:
			database.commit_D(self,sql)
		except:
			pass
		return wd_data
		'''
	
	def A_P(self,data,check,sensor=0):
		#AIR_PRESSURE			3
		node_id = data[0:4]
		sensor_type = data[6:8]
		recv_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		data_len = 4
		recv_data = data[8:8+2*data_len]
		pressure = str(int(recv_data,16)/1000) + 'KPa'
		pressure_value = int(recv_data,16)/1000
		try:
			p = Data.query.filter_by(node_id=node_id,sensor_type=sensor_type).first()
			p.recv_data = pressure
			p.time = recv_time
		except:
			p = Data(node_id,sensor_type,recv_time,pressure)
		finally:
			db.session.add(p)
			db.session.commit()
		pressure_value = proto_send.SensorValue(self,node_id,3,pressure_value,0)
		'''
		Date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		IP = data[0:2]
		AIR_PRESSURE_DATA = int(data[6:14],16)/1000
		Data = str(int(data[6:14],16)/1000) + ' kPa'
		if len(check) == 6:
			print('ctrl')
			pressure_value = proto_send.DSensorCtrlRsp(self,0,data[0:2],AIR_PRESSURE_DATA,0,sensor)
		else:
			pressure_value = proto_send.SensorValue(self,IP,3,AIR_PRESSURE_DATA,0)
		sql = "INSERT INTO A_P(Date,IP,Data)\
					VALUES ('%s','%s','%s')" % (Date,IP,Data)
		try:
			database.commit_D(self,sql)
		except:
			pass
		'''
		return pressure_value
		
	def A_L(self,data,check,sensor=0):
		#LIGHT				6
		node_id = data[0:4]
		sensor_type = data[6:8]
		recv_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		data_len = 4
		recv_data = data[8:8+2*data_len]
		light = str(int(recv_data,16)/1000) +'lux'
		light_value = int(recv_data,16)/1000
		try:
			l = Data.query.filter_by(node_id=node_id,sensor_type=sensor_type).first()
			l.recv_data = light
			l.time = recv_time
		except:
			l = Data(node_id,sensor_type,recv_time,light)
		finally:
			db.session.add(l)
			db.session.commit()
		light_value = proto_send.SensorValue(self,node_id,6,light_value,0)
		'''
		Date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		IP = data[0:2]
		AIR_LIGHT_DATA = int(data[6:14],16)/1000
		Data = str(int(data[6:14],16)) + ' lux'
		if len(check) == 6:
			print('ctrl')
			light_value = proto_send.DSensorCtrlRsp(self,0,data[0:2],AIR_LIGHT_DATA,0,sensor)
		else:
			light_value = proto_send.SensorValue(self,IP,6,AIR_LIGHT_DATA,0)
		sql = "INSERT INTO A_L(Date,IP,Data) VALUES ('%s','%s','%s')" % (Date,IP,Data)
		try:
			database.commit_D(self,sql)
		except:
			pass
		'''
		return light_value
		
		
	def S_T(self,data,check,sensor=0):
		#S_T		4
		node_id = data[0:4]
		sensor_type = data[6:8]
		recv_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		data_len = 2
		recv_data = data[8:8+2*data_len]
		d = Data(node_id,sensor_type,recv_time,recv_data)
		db.session.add(d)
		db.session.commit()
		'''
		Date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		IP = data[0:2]
		Temperature_Value = (int(data[6:8],16)*256+int(data[8:10],16))/100
		Temperature = str((int(data[6:8],16)*256+int(data[8:10],16))/100) + "C"
		if len(check) == 6:
			print('ctrl')
			temperature_value = proto_send.DSensorCtrlRsp(self,0,data[0:2],Temperature_Value,0,sensor)
		else:
			temperature_value = proto_send.SensorValue(self,IP,4,Temperature_Value,0)
		sql = "INSERT INTO S_T(Date,IP,Data)\
					VALUES ('%s','%s','%s')" % (Date,IP,Temperature)
		try:
			database.commit_D(self,sql)
		except:
			pass
		return temperature_value
		'''
			
	def S_H(self,data,check,sensor=0):
		#S_H		5
		node_id = data[0:4]
		sensor_type = data[6:8]
		recv_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		data_len = 2
		recv_data = data[8:8+2*data_len]
		d = Data(node_id,sensor_type,recv_time,recv_data)
		db.session.add(d)
		db.session.commit()
		#humanity_value = proto_send.SensorValue(self,IP,5,Humanity_Value,0)
		'''
		Date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		IP = data[0:2]
		Humanity_Value = (int(data[10:12],16)*256+int(data[12:14],16))/100
		Humanity = str((int(data[10:12],16)*256+int(data[12:14],16))/100) + "%"
		if len(check) == 6:
			print('ctrl')
			humanity_value = proto_send.DSensorCtrlRsp(self,0,data[0:2],Humanity_Value,0,sensor)
		else:
			humanity_value = proto_send.SensorValue(self,IP,5,Humanity_Value,0)
		sql = "INSERT INTO S_H(Date,IP,Data)\
					VALUES ('%s','%s','%s')" % (Date,IP,Humanity)
		try:
			database.commit_D(self,sql)
		except:
			pass
		return humanity_value
		'''
		
	def A_T(self,data,check,sensor=0):
		#A_T		1
		node_id = data[0:4]
		sensor_type = data[6:8]
		recv_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		data_len = 4
		recv_data = data[8:8+2*data_len]
		temp = str(int(recv_data,16)/1000) + '℃'
		temp_value = int(recv_data,16)/1000
		try:
			t = Data.query.filter_by(node_id=node_id,sensor_type=sensor_type).first()
			t.recv_data = temp
			t.time = recv_time
		except:
			t = Data(node_id,sensor_type,recv_time,temp)
		finally:
			db.session.add(t)
			db.session.commit()
		temperature_value = proto_send.SensorValue(self,node_id,1,temp_value,0)
		'''
		Date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		IP = data[0:2]
		Temperature_Value = int(data[6:14],16)/1000
		Temperature = str(Temperature_Value) + "C"
		if len(check) == 6:
			print('ctrl')
			temperature_value = proto_send.DSensorCtrlRsp(self,0,data[0:2],Temperature_Value,0,sensor)
		else:
			temperature_value = proto_send.SensorValue(self,IP,1,Temperature_Value,0)
		sql = "INSERT INTO A_T(Date,IP,Data)\
					VALUES ('%s','%s','%s')" % (Date,IP,Temperature)
		try:
			database.commit_D(self,sql)
		except:
			pass
		'''
		return temperature_value
		
			
	def A_H(self,data,check,sensor=0):
		#A_H		2
		node_id = data[0:4]
		sensor_type = data[6:8]
		recv_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		data_len = 4
		recv_data = data[16:16+2*data_len]
		humility = str(int(recv_data,16)/1000) + '%'
		humility_value = int(recv_data,16)/1000
		try:
			h = Data.query.filter_by(node_id=node_id,sensor_type=sensor_type).first()
			h.recv_data = humility
			h.time = recv_time
		except:
			h = Data(node_id,sensor_type,recv_time,humility)
		finally:
			db.session.add(h)
			db.session.commit()
		humanity_value = proto_send.SensorValue(self,node_id,2,humility_value,0)
		'''
		Date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		IP = data[0:2]
		Humanity_Value = int(data[14:22],16)/1000
		Humanity = str(Humanity_Value) + "%"
		if len(check) == 6:
			print('ctrl')
			humanity_value = proto_send.DSensorCtrlRsp(self,0,data[0:2],Humanity_Value,0,sensor)
		else:
			humanity_value = proto_send.SensorValue(self,IP,2,Humanity_Value,0)
		sql = "INSERT INTO A_H(Date,IP,Data)\
					VALUES ('%s','%s','%s')" % (Date,IP,Humanity)
		try:
			database.commit_D(self,sql)
		except:
			pass
		'''
		return humanity_value
		
		
	def S_PH(self,data,check,sensor=0):
		self.Local_Time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		print("S_PH")
		
	def Bat_AD(self,data,check,sensor=0):
		#BAT				10
		pass
		'''
		Date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		IP = data[0:2]
		Data = (int(data[6:8],16)/256)*3*2
		BAT_DATA = round(Data,2)
		Data = str(round(Data,2))
		print("IP: " + IP)
		print("Date: " + Date)
		print("Data: " + Data)
		print('\n')
		if len(check) == 6:
			print('ctrl')
			bat_value = proto_send.DSensorCtrlRsp(self,0,data[0:2],BAT_DATA,0,sensor)
		else:
			bat_value = proto_send.SensorValue(self,IP,10,BAT_DATA,0)
		sql = "INSERT INTO Bat_AD(Date,IP,Data)\
					VALUES ('%s','%s','%s')" % (Date,IP,Data)
		try:
			database.commit_D(self,sql)
		except:
			pass
		return bat_value
		'''
		
	def Sun_AD(self,data,check,sensor=0):
		#Sun				11
		pass
		'''
		Date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		IP = data[0:2]
		Data = (int(data[6:8],16)/256)*3*2
		Sun_Data = round(Data,2)
		Data = str(round(Data,2))
		print("IP: " + IP)
		print("Date: " + Date)
		print("Data: " + Data)
		print('\n')
		if len(check) == 6:
			print('ctrl')
			sun_value = proto_send.DSensorCtrlRsp(self,0,data[0:2],Sun_Data,0,sensor)
		else:
			sun_value = proto_send.SensorValue(self,IP,11,Sun_Data,0)
		sql = "INSERT INTO Sun_AD(Date,IP,Data)\
					VALUES ('%s','%s','%s')" % (Date,IP,Data)
		try:
			database.commit_D(self,sql)
		except:
			pass
		return sun_value
		'''



#来自串口中的检索，下面第一个表放在analysis_D中，同事更改一下serial_thread即可
Dict_Sensor = {\
	'12':analysis_D().A_P,\
	'13':analysis_D().A_L,\
	'20':analysis_D().S_T,\
	'10':analysis_D().A_T,\
	'21':analysis_D().S_H,\
	'11':analysis_D().A_H,\
	'22':analysis_D().S_PH,\
	'41':analysis_D().Bat_AD,\
	'42':analysis_D().Sun_AD,\
	'14':analysis_D().W_S,\
	'15':analysis_D().W_D}