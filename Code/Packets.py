typeToNum = {"Message": 0, "RequestInfo": 1, "NextHop": 2, "AddService": 3}

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

class RequestInfoPacket():
  def __init__(self, dest, forwarderName):
    self.type = typeToNum["RequestInfo"]

    self.dest = dest
    destByteStrs = dest.split(":")
    self.destBytes = [bytes(bytearray.fromhex(x)) for x in destByteStrs]

    self.forwarderName = forwarderName
    forwarderNameByteStrs = forwarderName.split(":")
    self.forwarderNameBytes = [bytes(bytearray.fromhex(x)) for x in forwarderNameByteStrs]
  
  def encode(self):
    # Store type of packet in first byte
    typeByte = (self.type).to_bytes(1, byteorder='big')
    encoding = typeByte

    for byte in self.destBytes:
      encoding += byte

    for byte in self.forwarderNameBytes:
      encoding += byte
      
    # Return packet bytes
    return encoding

  @classmethod
  def decode(cls, packet):
    dest = packet[1:4].hex(":")
    forwarderName = packet[4:7].hex(":")
    return cls(dest, forwarderName)

class NextHopPacket():
  def __init__(self, dest, nextHop):
    self.type = typeToNum["NextHop"]

    self.dest = dest
    destByteStrs = dest.split(":")
    self.destBytes = [bytes(bytearray.fromhex(x)) for x in destByteStrs]

    self.nextHop = nextHop 
  
  def encode(self):
    # Store type of packet in first byte
    typeByte = (self.type).to_bytes(1, byteorder='big')
    encoding = typeByte

    for byte in self.destBytes:
      encoding += byte

    encoding += str.encode(self.nextHop)

    # Return packet bytes
    return encoding

  @classmethod
  def decode(cls, packet):
    dest = packet[1:4].hex(":")
    nextHop = packet[4:].decode()
    return cls(dest, nextHop)

class AddServicePacket():
  def __init__(self, name, port, forwarderName):
    self.type = typeToNum["AddService"]

    self.name = name 
    nameByteStrs = name.split(":")
    self.nameBytes = [bytes(bytearray.fromhex(x)) for x in nameByteStrs]

    self.port = port

    self.forwarderName = forwarderName
    forwarderNameByteStrs = forwarderName.split(":")
    self.forwarderNameBytes = [bytes(bytearray.fromhex(x)) for x in forwarderNameByteStrs]
  
  def encode(self):
    # Store type of packet in first byte
    typeByte = (self.type).to_bytes(1, byteorder='big')
    encoding = typeByte

    for byte in self.nameBytes:
      encoding += byte

    encoding += (self.port).to_bytes(2, byteorder='big')

    for byte in self.forwarderNameBytes:
      encoding += byte

    # Return packet bytes
    return encoding

  @classmethod
  def decode(cls, packet):
    name = packet[1:4].hex(":")
    port = int.from_bytes(packet[4:6], byteorder='big')
    forwarderName = packet[6:9].hex(":")
    return cls(name, port, forwarderName)

numToClass = {0: MessagePacket, 1: RequestInfoPacket, 2: NextHopPacket, 3: AddServicePacket}

def decodePacket(packet):
  packetType = packet[0]
  if packetType not in numToClass:
    return None
  return numToClass[packetType].decode(packet)
