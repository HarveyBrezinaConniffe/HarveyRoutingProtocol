import socket
import Packets

PORT = 54321
CONTROLLER_IP = "172.50.0.2"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

# Map dest ID to next node IP
nextHop = None

myIP = input("> ")
print("Sending Hello to controller!")
sock.sendto(Packets.HelloPacket(myIP).encode(), (CONTROLLER_IP, PORT))

def recievePacket(data, addr):
  global nextHop
  print("PACKET INCOMING")
  packet = Packets.decodePacket(data)
  if packet == None:
    return
  if packet.type == Packets.typeToNum["Message"]:
    print("Recieving packet destined for {} with payload {}".format(packet.dest, packet.payload))
    print("Next hop is {}".format(nextHop))
    sock.sendto(data, (nextHop, PORT))
  if packet.type == Packets.typeToNum["NextHop"]:
    print("Recieving flow information")
    nextHop = packet.hopIP

while True:
  data, addr = sock.recvfrom(512)
  recievePacket(data, addr)
