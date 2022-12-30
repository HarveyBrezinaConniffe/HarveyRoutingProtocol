import socket
import Packets

PORT = 54321
CONTROLLER_IP = "172.50.0.0"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

myName = input("Forwarder Name> ")

# Store packets grouped by final destination
packetBuffer = {}

def recievePacket(data, addr):
  print("PACKET INCOMING")
  packet = Packets.decodePacket(data)

  if packet == None:
    return

  if packet.type == Packets.typeToNum["Message"]:
    print("Recieving packet destined for {} with payload {}".format(packet.dest, packet.payload))
    print("Buffering packet and asking controller for info.").
    if packet.dest not in packetBuffer:
      packetBuffer[packet.dest] = []
    packetBuffer[packet.dest].append(data) 
    reqPacket = Packets.RequestInfoPacket(packet.dest, myName)
    sock.send(reqPacket.encode())

while True:
  data, addr = sock.recvfrom(512)
  recievePacket(data, addr)
