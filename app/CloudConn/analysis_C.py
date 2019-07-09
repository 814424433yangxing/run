class analysis_C():
	def __init__(self):
		pass

	def Build_CMD(self,Node,Gate,sensor_lan,cmd_data,interval):
		try:
			if interval != 0:
				CMD_init = sensor_lan + '00'
				crc_before = Gate + CMD_init
				#CMD =  Node + Gate + CMD_init + crc.crc_modbus(self,CMD_init)
				CMD =  Node + Gate + CMD_init + self.crc_modbus(crc_before)
				return [CMD,sensor_lan]
		except:
			pass
	
	def Build_CMD_ctrl(self,ID,row):
		try:
			CMD_init = ID + row['Function'] + self.Dict[ID][1] + row['Register_L'] + row['Data_H'] + row['Data_L']
			CMD = CMD_init + crc.crc_modbus(self,CMD_init)
			return [CMD,row['Function_Num']]
		except:
			return False

	def crc_modbus(self,str1):
		data = bytearray.fromhex(str1)
		crc = 0xFFFF
		for pos in data:
			crc ^= pos
			for i in range(8):
				if ((crc & 1) != 0):
					crc >>= 1
					crc ^= 0xA001
				else:
					crc >>= 1
		hex_data = str(hex(((crc & 0xff) << 8) + (crc >> 8)))
		return hex_data[2:].zfill(4)