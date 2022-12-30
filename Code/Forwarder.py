import socket
import Packets

PORT = 54321
CONTROLLER_IP = "172.25.0.10"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

services = {}

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
    print("Buffering packet and asking controller for info.")
    if packet.dest in services:
      print("Recieved packet for service.")
      sock.sendto(data, (services[packet.dest][0], services[packet.dest][1]))
      return

    if packet.dest not in packetBuffer:
      packetBuffer[packet.dest] = []
    packetBuffer[packet.dest].append(data) 
    reqPacket = Packets.RequestInfoPacket(packet.dest, myName)
    sock.sendto(reqPacket.encode(), (CONTROLLER_IP, PORT))

  if packet.type == Packets.typeToNum["NextHop"]:
    print("Recieved next hop for packets destined for {} (Next hop is {})".format(packet.dest, packet.nextHop))
    if packet.dest not in packetBuffer:
      packetBuffer[packet.dest] = []

    for bufferedPacket in packetBuffer[packet.dest]:
      print("Sending buffered packet")
      sock.sendto(bufferedPacket, (packet.nextHop, PORT))
    packetBuffer[packet.dest] = []

  if packet.type == Packets.typeToNum["AddService"]:
    services[packet.name] = [addr[0], packet.port]
    controllerUpdatePacket = Packets.AddServicePacket(packet.name, packet.port, myName)
    sock.sendto(controllerUpdatePacket.encode(), (CONTROLLER_IP, PORT))

while True:
  data, addr = sock.recvfrom(512)
  recievePacket(data, addr)
