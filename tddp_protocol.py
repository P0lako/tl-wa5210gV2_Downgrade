import socket
import re

from winregistry import hexdump
from structure import Structure
import struct

class TDDP(Structure):
    structure = (
       ('version','B=0x1'),
       ('type','B=0'),       
       ('code','B=0'),
       ('replyInfo','B=0'),
       ('packetLength','>L=0'),
       ('pktID','<H=1'),
       ('subType','B=0'),
       ('reserved','B=0'),
       ('payload',':=""'),        
    )
    def printPayload(self):
		print self.getPayloadAsString()
	
    def getPayloadAsString(self):
        s=''
        for i in range(len(self['payload'])):
            s += "%.2X" % struct.unpack("B", self['payload'][i])[0]
        return s


class TDDPRequestsPacketBuilder(object):
	SET_CONFIG = 1
	GET_CONFIG = 2
	CMD_SYS0_PR = 3
	GET_SERIAL_NUMBER = 5
	
	GET_PRODUCT_ID = 10	
	
	def getRequestPacket(self):
		tddp = TDDP()
		tddp['version'] = 1
		tddp['replyInfo'] = 1		
		return tddp
	
	def getConfigPacket(self):
		tddp = self.getRequestPacket()
		tddp['type'] = self.GET_CONFIG 
		tddp['payload'] = ('\x00'*0x10) + 'all'
		tddp['packetLength'] = len(tddp['payload'])
		return tddp

	def setConfigPacket(self, trail):
		tddp = self.getRequestPacket()
		tddp['type'] = self.SET_CONFIG 
		tddp['payload'] = ('\x00'*0x10) + trail
		tddp['packetLength'] = len(tddp['payload'])
		return tddp
		
	def getSerialNumberPacket(self):
		tddp = self.getRequestPacket()
		tddp['type'] = self.GET_SERIAL_NUMBER
		return tddp

	def getProductIDPacket(self):
		tddp = self.getRequestPacket()
		tddp['type'] = self.GET_PRODUCT_ID
		return tddp
	
	def CMD_SYS0_PR_Packet(self, trail):
		tddp = self.getRequestPacket()
		tddp['type'] = self.CMD_SYS0_PR
		tddp['replyInfo'] = 2
		tddp['payload'] = ('\x00'*0x10)
		tddp['packetLength'] = len(tddp['payload'])
		tddp['payload'] += trail
		return tddp
		

class TPLINKConfig(object):
	def __init__(self, aConfig):
		self.__parseConfig(aConfig)
		
	def __sanitizeKeyValue(self, k, v):
		k = k.replace("\r", "")
		k = k.replace("\n", "")
		
		v = v.replace("\r", "")
		v = v.replace("\n", "")
		
		return k,v
		
	def __parseConfig(self, aConfig):
		self.__key_order = []
		self.Header = aConfig[:0x10]
		pending = aConfig[0x10:]
		k_v = re.findall("(.*?) (.*)", pending)
		
		for k, v in k_v:
			k,v = self.__sanitizeKeyValue(k,v)
			real_value = v.split(" ")
			if len(real_value) == 1:
				real_value = real_value[0]
				
			self.__dict__[k] = real_value
			self.__key_order.append(k)
			
	def __str__(self):
		cfg = []
		cfg.append(self.Header)
		
		for k in self.__key_order:
			value = self.__dict__[k]

			if not isinstance(value, basestring):
				str_value = " ".join(value)
			else:
				str_value = value
			
			line = "%s %s" % (k, str_value)
			
			cfg.append(line) 
		
		
		str_cfg =  "\r\n".join(cfg)
		
		return str_cfg
		
class TDDPSessionV1(object):
	def __init__(self, ip, port=1040):
		self.ip = ip
		self.port = port
		self.req_buidler = TDDPRequestsPacketBuilder()

	def send(self, aPacket):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.conn.sendto(str(aPacket), (self.ip, self.port))
		self.conn.close()
		
	def recv(self, n):
		udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		udp.bind(('', 61000))
		data, addr = udp.recvfrom(n)
		return TDDP(data)
	
	def _send_and_recv(self, packet, n):
		self.send(packet)
		return self.recv(n)
	
	#####################################
	def getConfig(self):
		c_packet = self.req_buidler.getConfigPacket()
		return TPLINKConfig(self._send_and_recv(c_packet, 50000)['payload'])
		
	def getSerialNumber(self):
		c_packet = self.req_buidler.getSerialNumberPacket()
		return self._send_and_recv(c_packet, 50000).getPayloadAsString()
		
	def getProductID(self):
		c_packet = self.req_buidler.getProductIDPacket()
		return self._send_and_recv(c_packet, 50000).getPayloadAsString()
		
	def setInitState(self):
		c_packet = self.req_buidler.CMD_SYS0_PR_Packet("init")
		return self._send_and_recv(c_packet, 50000)
		
	def save(self):
		c_packet = self.req_buidler.CMD_SYS0_PR_Packet("save")
		self._send_and_recv(c_packet, 50000)
		
	def reboot(self):
		c_packet = self.req_buidler.CMD_SYS0_PR_Packet("reboot")
		self._send_and_recv(c_packet, 50000)

	def clr_dos(self):
		c_packet = self.req_buidler.CMD_SYS0_PR_Packet("clr_dos")
		self._send_and_recv(c_packet, 50000)
		
	def setConfig(self, aConfig):
		c_packet = self.req_buidler.setConfigPacket(str(aConfig))
		self._send_and_recv(c_packet, 50000)
		