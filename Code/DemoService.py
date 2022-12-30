import socket
import Packets

PORT = 54321

setupSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

nearestNode = input("Nearest forwarder> ")

serviceName = input("Service Name> ")
servicePort = int(input("Service Port> "))

setupPacket = Packets.AddServicePacket(serviceName, servicePort, "00:00:00")
setupSock.sendto(setupPacket.encode(), (nearestNode, PORT))

print("Binding to {}".format(servicePort))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", servicePort))

def recievePacket(data, addr):
  print("PACKET INCOMING")
  packet = Packets.decodePacket(data)

  if packet == None:
    return
  
  if packet.type == Packets.typeToNum["Message"]:
    print("Recieved Message!")
    print(packet.payload)

while True:
  data, addr = sock.recvfrom(512)
  recievePacket(data, addr)
