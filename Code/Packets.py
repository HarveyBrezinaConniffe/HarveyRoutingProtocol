typeToNum = {"Message": 0}

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

numToClass = {0: MessagePacket}

def decodePacket(packet):
	packetType = packet[0]
	if packetType not in numToClass:
		return None
	return numToClass[packetType].decode(packet)
