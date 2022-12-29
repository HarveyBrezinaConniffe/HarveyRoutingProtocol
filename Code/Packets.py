typeToNum = {"Message": 0, "Hello": 1, "NextHop": 2}

class MessagePacket():
	def __init__(self, dest, payload):
		self.type = typeToNum["Message"]
		self.dest = dest
		destByteStrs = dest.split(":")
		self.destBytes = [bytes(bytearray.fromhex(x)) for x in destByteStrs]
		self.payload = payload
	
	def encode(self):
		# Store type of packet in first byte
		typeByte = (self.type).to_bytes(1, byteorder='big')
		encoding = typeByte
		for byte in self.destBytes:
			encoding += byte
		encoding += self.payload
		# Return packet bytes
		return encoding

	@classmethod
	def decode(cls, packet):
		# Everything after type byte is filename	
		dest = packet[1:4].hex(":")
		payload = packet[4:]
		return cls(dest, payload)

class HelloPacket():
	def __init__(self, routerIP):
		self.type = typeToNum["Hello"]
		self.routerIP = routerIP
	
	def encode(self):
		# Store type of packet in first byte
		typeByte = (self.type).to_bytes(1, byteorder='big')
		encoding = typeByte
		encoding += str.encode(self.routerIP)
		# Return packet bytes
		return encoding

	@classmethod
	def decode(cls, packet):
		# Everything after type byte is filename	
		routerIP = packet[1:].decode()
		return cls(routerIP)

class NextHopPacket():
	def __init__(self, hopIP):
		self.type = typeToNum["NextHop"]
		self.hopIP = hopIP
	
	def encode(self):
		# Store type of packet in first byte
		typeByte = (self.type).to_bytes(1, byteorder='big')
		encoding = typeByte
		encoding += str.encode(self.hopIP)
		# Return packet bytes
		return encoding

	@classmethod
	def decode(cls, packet):
		# Everything after type byte is filename	
		hopIP = packet[1:].decode()
		return cls(hopIP)

numToClass = {0: MessagePacket, 1: HelloPacket, 2: NextHopPacket}

def decodePacket(packet):
	packetType = packet[0]
	if packetType not in numToClass:
		return None
	return numToClass[packetType].decode(packet)
